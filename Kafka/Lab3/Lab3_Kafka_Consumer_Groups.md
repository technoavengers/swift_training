
# ✅ Lab 18: Working with Kafka Consumer Groups

🕒 **Estimated Time**: 15 minutes

---

## 🎯 Objective

This lab will teach you how Kafka consumer groups work. You'll observe how messages are distributed among multiple consumers in the same group and how group coordination behaves.

---

## 🛠️ Prerequisites

- Kafka and Zookeeper are running (`start-kafka.sh`)
- Topic created: `group-topic`
- Kafka CLI tools available in `~/kafka/bin`

---

## ☘️ Step 1: Create a Topic with Multiple Partitions

```bash
~/kafka/bin/kafka-topics.sh --create   --bootstrap-server localhost:9092   --replication-factor 1   --partitions 3   --topic group-topic
```

---


# Terminal 1

## ☘️ Step 2: Open  Terminal Windows and Start a Consumers in a Group


```bash
~/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic group-topic   --group demo-group
```

---

## ☘️ Step 4: Observe Partition Assignment

Open a new terminal and run:

```bash
~/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group demo-group
```

This shows:
- Group ID
- Topic
- Partition
- Current offset
- Lag
- Assigned consumer

---

# Terminal 2

## ☘️ Step 5: Add a Second Consumer

Open a second terminal and run:


```bash
~/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic group-topic   --group demo-group

```


## ☘️ Step 6: Observe Partition Assignment

Open a new terminal and run:

```bash
~/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group demo-group
```

This time you will see in client_id, one partition is assigned to one consumer and 2 partition assigned to another consumer

# Terminal 3

## ☘️ Step 7: Add a Third Consumer

Open a second terminal and run:

```bash
~/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic group-topic   --group demo-group
```

## ☘️ Step 8: Observe Partition Assignment

Open a new terminal and run:

```bash
~/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group demo-group
```

This time you will see every consumer has been assigned one partition



## 🧹 Step 7: Clean Up

```bash
~/kafka/bin/kafka-topics.sh --delete --bootstrap-server localhost:9092 --topic group-topic
```


---

## ✅ End of Lab

You now understand:
- How consumer groups share partitions
- Offset tracking and lag
- Group isolation behavior
