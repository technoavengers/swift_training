
# ✅ Lab 16: Getting Started with Apache Kafka CLI

🕒 **Estimated Time**: 20–25 minutes

---

## 🎯 Objective

In this lab, you'll learn to start Kafka from a binary installation using a custom script, verify the cluster status, and perform basic operations using Kafka CLI tools like creating, listing, and describing topics.

---

## 📦 Prerequisites

- Kafka binary is already extracted under the home directory: `~/kafka`
- Java is installed
- Zookeeper and Kafka are not yet running

---

## 🪜 Step 1: Start Kafka Using `start-kafka.sh`

Run below command in Vscode terminal to start kafka and Zookeeper.


```bash
~/kafka/start-kafka.sh
```

---

## 🔍 Step 2: Check Zookeeper and Kafka Logs
Ensure there are no errors and both services have started successfully.

```bash
tail -f ~/kafka/zookeeper.log
```
Press Ctrl+C to exit

```bash
tail -f ~/kafka/kafka.log
```
Press Ctrl+C to exit


---

## 📋 Step 3: Check Kafka Cluster Info

List broker topics:

```bash
~/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

You may see no output if no topics exist yet.

---

## 🧪 Step 4: Create a New Topic

```bash
~/kafka/bin/kafka-topics.sh --create   --bootstrap-server localhost:9092   --replication-factor 1   --partitions 2   --topic test-topic
```

---

## 📜 Step 5: Describe a Topic

```bash
~/kafka/bin/kafka-topics.sh --describe   --bootstrap-server localhost:9092   --topic test-topic
```

This shows partition details, leader, replicas, and ISR.

---

## 📂 Step 6: List All Topics

```bash
~/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

---

## 🧹 Step 7: Delete a Topic (Optional)

```bash
~/kafka/bin/kafka-topics.sh --delete --bootstrap-server localhost:9092 --topic test-topic
```

> Deletion must be enabled in your Kafka config with: `delete.topic.enable=true`

---

## ✅ End of Lab

You have now:
- Started Kafka using a script
- Created, listed, and described Kafka topics
- Verified the cluster is operational

You’re ready to move on to producing and consuming messages!
