import React, { useEffect, useState } from "react";
import { StyleSheet, Text, View, Button } from "react-native";

export default function App() {
  const [data, setData] = useState("Loading...");

  const fetchData = async () => {
    try {
      const res = await fetch("https://api.kubu-hai.com/data"); // your FastAPI endpoint
      const json = await res.json();
      setData(JSON.stringify(json));
    } catch (err) {
      setData("Error: " + err.message);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>🚀 My AI App</Text>
      <Text style={styles.data}>{data}</Text>
      <Button title="Refresh" onPress={fetchData} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center" },
  title: { fontSize: 22, fontWeight: "bold", marginBottom: 20 },
  data: { margin: 20, textAlign: "center" },
});
