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

    // 2. Определение ID платежной системы
    let paymentSystemId = process.env.SENDPULSE_PAYMENT_SYSTEM_ID;

    if (!paymentSystemId) {
      console.log('SENDPULSE_PAYMENT_SYSTEM_ID не задан. Запрашиваем методы оплаты через API...');
      const methodsRes = await fetch('https://api.sendpulse.com/crm/v1/payments/user-payment-methods', {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });

      if (methodsRes.ok) {
        const methodsData = await methodsRes.json();
        console.log('Доступные методы оплаты:', JSON.stringify(methodsData));
        const list = Array.isArray(methodsData) ? methodsData : (methodsData.result || methodsData.data || []);
        
        // Находим первый активный метод оплаты (статус 1 или 2 означает активный)
        const activeMethod = list.find(m => m.status === 1 || m.status === 2 || m.active === true || m.status === 'active') || list[0];
        if (activeMethod) {
          paymentSystemId = activeMethod.paymentId || activeMethod.id;
          console.log(`Автоматически выбран платежный метод: ${activeMethod.name || paymentSystemId} (ID: ${paymentSystemId})`);
        }
      }
    }

    if (!paymentSystemId) {
      return res.status(400).json({
        success: false,
        error: 'В аккаунте SendPulse не найдено подключенных платежных систем. Подключите платежную систему в разделе "Прием оплат" или укажите SENDPULSE_PAYMENT_SYSTEM_ID в переменных окружения.'
      });
    }

    // 3. Создание контакта в CRM
    // Никнейм Телеграм и UTM-метки сохраняем в имени для наглядности в CRM
    let utmString = '';
    if (utm && typeof utm === 'object') {
      const parts = [];
      if (utm.utm_source) parts.push(utm.utm_source);
      if (utm.utm_medium) parts.push(utm.utm_medium);
      if (utm.utm_campaign) parts.push(utm.utm_campaign);
      
      if (parts.length > 0) {
        utmString = ` [utm: ${parts.join(' / ')}]`;
      }
    }

    const contactName = `${name} (${telegram})${utmString}`;

    const contactRes = await fetch('https://api.sendpulse.com/crm/v1/contacts', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: contactName,
        phones: [
          {
            phone: phone,
            type: 'mobile'
          }
        ]
      })
    });

    let contactId;
    const contactData = await contactRes.json();

    if (contactRes.ok && contactData) {
      contactId = contactData.id || (contactData.data && contactData.data.id);
    } else {
      console.error('Ошибка создания контакта в CRM:', JSON.stringify(contactData));
      // Если возникла ошибка, попробуем поискать существующий по номеру телефона
      // Или если контакт уже есть, но API выдал ошибку дублирования.
      // Нам нужен любой рабочий ID контакта для генерации ссылки.
      // Попробуем продолжить, если ID все-таки вернулся в структуре ошибки, либо возвращаем ошибку.
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

    // 4. Генерация ссылки на оплату
    const paymentPayload = {
      contact_id: Number(contactId) || contactId,
      payment_system_id: Number(paymentSystemId) || paymentSystemId,
      amount: 0.99,
      currency: 'EUR',
      description: 'Церемония Тишины'
    };

    console.log('Отправка запроса на создание платежа:', JSON.stringify(paymentPayload));

    const paymentRes = await fetch('https://api.sendpulse.com/crm/v1/payments/contact-generate-payment-link', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(paymentPayload)
    });

    const paymentData = await paymentRes.json();

    if (!paymentRes.ok) {
      console.error('Ошибка генерации ссылки на оплату:', JSON.stringify(paymentData));
      return res.status(502).json({
        success: false,
        error: 'Не удалось сгенерировать ссылку на оплату в SendPulse.',
        details: paymentData
      });
    }

    const paymentUrl = paymentData.payment_link || 
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
