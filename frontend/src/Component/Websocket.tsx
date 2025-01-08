import { useState, useEffect, useRef } from "react";
import toast, { Toaster } from "react-hot-toast";

interface Message {
  status: boolean;
  message: string;
  is_valid: boolean;
}

interface WebSocketComponentProps {
  setIsTableDataValid: () => void;
}

const WebSocketComponent = ({ 
  setIsTableDataValid }: WebSocketComponentProps) => {
  const [messages, setMessages] = useState<string[]>([]);
  const [isConnected, setIsConnected] = useState(true);
  const ws = useRef<WebSocket | null>(null);
  const [socket, setSocket] = useState(true);
  const notify = (message: string) => toast.success(message, {duration: 10000});

  useEffect(() => {
    if (socket) {
      // Create WebSocket connection
      console.log("WebSocketComponent mounted");

      // if (!ws.current) {
      ws.current = new WebSocket("ws://localhost:8000/ws");

      //handle successfull connection
      ws.current.onopen = () => {
        console.log("WebSocket Connected");
        setIsConnected(true);
        setMessages(() => ["WebSocket Connected"]);
      };

      ws.current.onerror = (error) => {
        console.error("WebSocket Error:", error);
      };

      ws.current.onmessage = (event: MessageEvent) => {

        const data = JSON.parse(event.data) as Message;
        console.log("message received from websocket");
        notify(data.message);

        setIsTableDataValid();

        // 

        try {
          setMessages(() => [data.message]);
        } catch (error) {
          console.error("Error parsing message:", error);
        }
      };

      ws.current.onclose = () => {
        console.log("WebSocket Disconnected");
        setIsConnected(false);
        setMessages(() => ["WebSocket Disconnected"]);
      };

      // Clean up function
      return () => {
        if (ws.current) {
          ws.current.close();
        }
      };
    }

    // }
  }, [socket]); // Empty dependency array ensures this effect runs only once on mount

  return (
    <div>
      <Toaster position="top-right" />
      {/* <h2>WebSocket Messages</h2>
      <p>Connection status: {isConnected ? "Connected" : "Disconnected"}</p>
      {messages.length > 0 ? (
        <ul>
          {messages.map((message, index) => (
            <li key={index}>{message}</li>
          ))}
        </ul>
      ) : (
        <p>No messages received yet.</p>
      )} */}
    </div>
  );
};

export default WebSocketComponent;
