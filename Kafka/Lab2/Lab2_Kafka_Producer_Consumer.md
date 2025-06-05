
# ✅ Lab 2: Producing and Consuming Messages with Kafka CLI

🕒 **Estimated Time**: 20–25 minutes

---

## 🎯 Objective

In this lab, you'll learn to use `kafka-console-producer.sh` and `kafka-console-consumer.sh` to send and receive messages from a Kafka topic. This is essential for verifying message flow in a Kafka setup.

---

## 🛠️ Prerequisites

- Kafka is running (started using `start-kafka.sh`)
- `~/kafka/bin` directory contains Kafka CLI tools
- Java is installed and environment is set up

---

## ☘️ Step 1: Create a Topic

```bash
cd ~/kafka
~/kafka/bin/kafka-topics.sh --create   --bootstrap-server localhost:9092   --replication-factor 1   --partitions 1   --topic demo-topic
```

---

## ☘️ Step 2: Start the Kafka Console Consumer

Start the consumer and let it wait for messages:

```bash
~/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic demo-topic   --from-beginning
```

Keep this terminal open. It will display messages as they are produced.

---

## ☘️ Step 3: Open a New Terminal and Start the Kafka Console Producer

```bash
cd ~/kafka
~/kafka/bin/kafka-console-producer.sh   --broker-list localhost:9092   --topic demo-topic
```

Start typing messages and hit Enter to send each message. Example:

```
Hello Kafka!
This is a message.
Kafka CLI lab is working!
```

You should see these messages instantly appear in the consumer terminal.


---

## 🧹 Step 5: Clean Up

You can stop the producer and consumer with `Ctrl+C`.

To delete the topic:

```bash
~/kafka/bin/kafka-topics.sh --delete --bootstrap-server localhost:9092 --topic demo-topic
---

## ✅ End of Lab

You have learned how to:
- Create a Kafka topic
- Produce messages from CLI
- Consume messages in real-time
