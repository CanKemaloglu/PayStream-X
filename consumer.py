from confluent_kafka import Consumer
import json

# Kafka bağlantı ayarları
conf = {
    'bootstrap.servers': "127.0.0.1:9092",
    'group.id': "paystream_analytics",
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['payments'])

total_revenue = 0.0
transaction_count = 0

print("📊 PayStream-X Analiz Paneli Başladı...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        if msg.error():
            print(f"Hata: {msg.error()}")
            continue

        # Gelen veriyi çöz (Decode)
        data = json.loads(msg.value().decode('utf-8'))
        
        # Basit Analiz: Ciro ve İşlem Sayısı Hesapla
        total_revenue += data['amount']
        transaction_count += 1
        
        # Sonucu ekrana yazdır (Gerçek zamanlı Dashboard mantığı)
        print(f"✅ Yeni İşlem: {data['order_id']} | Sağlayıcı: {data['provider']} | Tutar: {data['amount']} {data['currency']}")
        print(f"--- Toplam İşlem: {transaction_count} | Toplam Ciro (Sanal): {round(total_revenue, 2)} ---")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
