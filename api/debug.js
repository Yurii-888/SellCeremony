export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');

  try {
    const clientId = process.env.SENDPULSE_CLIENT_ID;
    const clientSecret = process.env.SENDPULSE_CLIENT_SECRET;

    if (!clientId || !clientSecret) {
      return res.status(500).json({
        error: 'SENDPULSE_CLIENT_ID or SENDPULSE_CLIENT_SECRET not configured in Vercel env.'
      });
    }

    // 1. Get access token
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
      return res.status(502).json({ error: 'Auth failed', details: errorText });
    }

    const tokenData = await tokenRes.json();
    const accessToken = tokenData.access_token;

    // 2. Fetch payment systems
    const methodsRes = await fetch('https://api.sendpulse.com/crm/v1/payments/user-payment-methods', {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });

    const status = methodsRes.status;
    const headers = Object.fromEntries(methodsRes.headers.entries());
    let data;
    try {
      data = await methodsRes.json();
    } catch (e) {
      data = await methodsRes.text();
    }

    return res.status(200).json({
      success: true,
      apiStatus: status,
      paymentSystemIdEnv: process.env.SENDPULSE_PAYMENT_SYSTEM_ID,
      data
    });

  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
