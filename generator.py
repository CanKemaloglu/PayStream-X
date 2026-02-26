from confluent_kafka import Producer
import json
import time
import random

# Kafka'ya bağlanıyoruz
conf = {'bootstrap.servers': "localhost:9092"}
producer = Producer(conf)

def rapor(err, msg):
    if err: print(f"Hata: {err}")
    else: print(f"Veri Gönderildi: {msg.topic()} - {msg.value().decode('utf-8')}")

print("🚀 PayStream-X Ödeme Akışı Başladı (Durdurmak için Ctrl+C)...")

providers = ['Adyen', 'Stripe', 'Iyzico', 'Braintree']
currencies = ['EUR', 'USD', 'TRY', 'GBP']

while True:
    data = {
        "order_id": random.randint(100000, 999999),
        "amount": round(random.uniform(50, 2000), 2),
        "currency": random.choice(currencies),
        "provider": random.choice(providers),
        "status": "SUCCESS",
        "timestamp": time.time()
    }
    
    # Veriyi 'payments' kanalına gönder
    producer.produce('payments', json.dumps(data).encode('utf-8'), callback=rapor)
    producer.flush()
    time.sleep(2) # 2 saniyede bir yeni ödeme gönder
