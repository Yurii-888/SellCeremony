export default async function handler(req, res) {
  // Разрешаем только POST запросы
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(200).end();
  }

  res.setHeader('Access-Control-Allow-Origin', '*');

  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Метод не поддерживается. Разрешен только POST.' });
  }

  try {
    const { name, phone, telegram, utm } = req.body;

    // Валидация входных данных
    if (!name || !phone || !telegram) {
      return res.status(400).json({ success: false, error: 'Необходимо заполнить все поля: Имя, Телефон, Telegram.' });
    }

    const clientId = process.env.SENDPULSE_CLIENT_ID;
    const clientSecret = process.env.SENDPULSE_CLIENT_SECRET;

    if (!clientId || !clientSecret) {
      return res.status(500).json({
        success: false,
        error: 'Внутренняя ошибка сервера: не настроены ключи API (SENDPULSE_CLIENT_ID, SENDPULSE_CLIENT_SECRET) в переменных окружения Vercel.'
      });
    }

    // 1. Получение access_token
    const tokenRes = await fetch('https://api.sendpulse.com/oauth/access_token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        grant_type: 'client_credentials',
        client_id: clientId,
        client_secret: clientSecret
      })
    });

    if (!tokenRes.ok) {
      const errorText = await tokenRes.text();
      console.error('Ошибка авторизации в SendPulse:', errorText);
      return res.status(502).json({ success: false, error: 'Не удалось авторизоваться в платежном сервисе SendPulse.' });
    }

    const tokenData = await tokenRes.json();
    const accessToken = tokenData.access_token;

    if (!accessToken) {
      return res.status(502).json({ success: false, error: 'Не получен токен авторизации от SendPulse.' });
    }

    // 2. Определение ID и типа платежной системы
    let paymentSystemId = process.env.SENDPULSE_PAYMENT_SYSTEM_ID;
    let paymentType = '';

    console.log('Запрашиваем методы оплаты через API...');
    const methodsRes = await fetch('https://api.sendpulse.com/crm/v1/payments/user-payment-methods', {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });

    if (methodsRes.ok) {
      const methodsData = await methodsRes.json();
      console.log('Доступные методы оплаты:', JSON.stringify(methodsData));
      const list = Array.isArray(methodsData) ? methodsData : (methodsData.result || methodsData.data || []);
      
      let selectedMethod;
      if (paymentSystemId) {
        selectedMethod = list.find(m => String(m.paymentId || m.id) === String(paymentSystemId));
      }
      
      if (!selectedMethod) {
        // Находим активный метод оплаты (статус 1 или 2 означает активный)
        selectedMethod = list.find(m => m.status === 1 || m.status === 2 || m.active === true || m.status === 'active' || String(m.status) === '2') || list[0];
      }

      if (selectedMethod) {
        paymentSystemId = selectedMethod.paymentId || selectedMethod.id;
        paymentType = selectedMethod.paymentType || selectedMethod.type || 'Wayforpay';
        console.log(`Выбран платежный метод: ${selectedMethod.name || paymentSystemId} (Тип: ${paymentType}, ID: ${paymentSystemId})`);
      }
    }

    if (!paymentSystemId) {
      return res.status(400).json({
        success: false,
        error: 'В аккаунте SendPulse не найдено подключенных платежных систем. Подключите платежную систему в разделе "Прием оплат" или укажите SENDPULSE_PAYMENT_SYSTEM_ID в переменных окружения.'
      });
    }

    // 3. Создание контакта в CRM
    const cleanPhone = phone.replace(/\D/g, ''); // Удаляем любые символы, кроме цифр

    // Формируем массив кастомных атрибутов (полей) контакта
    const attributes = [];
    if (telegram) {
      attributes.push({ name: 'Telegram', type: 0, value: telegram });
    }
    if (utm && typeof utm === 'object') {
      if (utm.utm_source) attributes.push({ name: 'utm_source', type: 0, value: utm.utm_source });
      if (utm.utm_medium) attributes.push({ name: 'utm_medium', type: 0, value: utm.utm_medium });
      if (utm.utm_campaign) attributes.push({ name: 'utm_campaign', type: 0, value: utm.utm_campaign });
      if (utm.utm_content) attributes.push({ name: 'utm_content', type: 0, value: utm.utm_content });
      if (utm.utm_term) attributes.push({ name: 'utm_term', type: 0, value: utm.utm_term });
    }

    const contactRes = await fetch('https://api.sendpulse.com/crm/v1/contacts', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        firstName: name,
        lastName: '',
        phones: [ cleanPhone ],
        attributes: attributes.length > 0 ? attributes : undefined
      })
    });

    let contactId;
    const contactData = await contactRes.json();

    if (contactRes.ok && contactData) {
      contactId = contactData.id || (contactData.data && contactData.data.id);
    } else {
      console.error('Ошибка создания контакта в CRM:', JSON.stringify(contactData));
      // Попробуем продолжить, если ID вернулся в структуре ошибки
      contactId = contactData.id || (contactData.data && contactData.data.id);
    }

    if (!contactId) {
      return res.status(502).json({
        success: false,
        error: 'Не удалось создать или найти контакт в CRM SendPulse.',
        details: contactData
      });
    }

    console.log(`Контакт успешно создан/найден. ID: ${contactId}`);

    // 4. Создание сделки в CRM
    const dealPayload = {
      pipelineId: 177532,
      stepId: 617504,
      name: `Церемония Тишины - ${name}`,
      price: 0.99,
      currency: 'EUR',
      contact: [ Number(contactId) || contactId ]
    };

    console.log('Отправка запроса на создание сделки:', JSON.stringify(dealPayload));

    const dealRes = await fetch('https://api.sendpulse.com/crm/v1/deals', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dealPayload)
    });

    const dealData = await dealRes.json();

    if (!dealRes.ok) {
      console.error('Ошибка создания сделки в CRM:', JSON.stringify(dealData));
      return res.status(502).json({
        success: false,
        error: 'Не удалось создать сделку в CRM SendPulse.',
        details: dealData
      });
    }

    const dealId = dealData.id || (dealData.data && dealData.data.id);

    if (!dealId) {
      console.error('API SendPulse не вернул ID сделки в ответе:', JSON.stringify(dealData));
      return res.status(502).json({
        success: false,
        error: 'Не получен идентификатор созданной сделки.',
        details: dealData
      });
    }

    console.log(`Сделка успешно создана. ID: ${dealId}`);

    // 5. Генерация ссылки на оплату на основе сделки
    const date = new Date();
    date.setDate(date.getDate() + 3); // Ссылка действительна 3 дня
    const untilDate = date.toISOString().split('T')[0];

    const paymentPayload = {
      paymentCategory: 2, // personalPayment
      paymentType: paymentType,
      paymentId: String(paymentSystemId),
      contactId: Number(contactId),
      pipelineId: 177532,
      stepId: 617504,
      dealId: Number(dealId),
      price: 0.99,
      currency: 'EUR',
      untilDate: untilDate,
      description: 'Церемония Тишины'
    };

    console.log('Отправка запроса на создание платежа сделки:', JSON.stringify(paymentPayload));

    const paymentRes = await fetch('https://api.sendpulse.com/crm/v1/payments/deal-generate-payment-link', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(paymentPayload)
    });

    const paymentData = await paymentRes.json();

    if (!paymentRes.ok) {
      console.error('Ошибка генерации ссылки на оплату для сделки:', JSON.stringify(paymentData));
      return res.status(502).json({
        success: false,
        error: 'Не удалось сгенерировать ссылку на оплату в SendPulse.',
        details: paymentData
      });
    }

    const paymentUrl = (paymentData.data && paymentData.data.link) || 
                       paymentData.payment_link || 
                       paymentData.paymentLink || 
                       (paymentData.data && (paymentData.data.payment_link || paymentData.data.paymentLink)) ||
                       (paymentData.result && paymentData.result.payment_link);

    if (!paymentUrl) {
      console.error('API SendPulse не вернул ссылку на оплату в ответе:', JSON.stringify(paymentData));
      return res.status(502).json({
        success: false,
        error: 'Не получен адрес страницы оплаты от платежной системы.',
        details: paymentData
      });
    }

    console.log(`Платежная ссылка успешно сгенерирована: ${paymentUrl}`);

    // Возвращаем ссылку на фронтенд
    return res.status(200).json({ success: true, paymentUrl });

  } catch (error) {
    console.error('Критическая ошибка в обработчике платежа:', error);
    return res.status(500).json({ success: false, error: 'Произошла непредвиденная ошибка на сервере: ' + error.message });
  }
}
