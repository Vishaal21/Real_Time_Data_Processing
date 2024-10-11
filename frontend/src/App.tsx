import { useEffect, useState } from "react";
import "./App.css";

import StockMarketChart from "./CandleStickChart";
import axios from "axios";
import TableContainer from "@mui/material/TableContainer";
import {
  Card,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import data from "./data.json";
import WebSocketComponent from "./Component/Websocket";
import LoadingComponent from "./Component/Loading";

interface FileMetadata {
  file_size: string;
  file_name: string;
  file_path: string | null;
  upload_date: string | null;
  created_at: string;
  id: number;
  file_type: string;
  is_valid: boolean | null;
  validation_message: string | null;
  updated_at: string;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [fileMetadataList, setFileMetadataList] = useState<FileMetadata[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [chartView, setChartView] = useState(false);
  const [idChart, setIdChart] = useState<number | null>();
  const [onSocket, setOnSocket] = useState(false);
  const [isTableDataValid, setIsTableDataValid] = useState(true);

  const options: Intl.DateTimeFormatOptions = {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: true,
  };

  const fetchFileMetadata: any = async () => {
    try {
      const response = await axios.get<FileMetadata[]>(
        "http://localhost:8000/api/v1/get_file_metadata"
      );
      if (response.status == 200 || response.status == 201) {
        setFileMetadataList(response.data);
        console.log(response.data);
      }
    } catch (err) {
      alert(err);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    fetchFileMetadata();
    setOnSocket(true);
  }, []);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    console.log(selectedFile);
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (file == null) {
      alert("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);
    try {
      const response = await axios.post(
        "http://localhost:8000/api/v1/upload_file",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      // show loading that file is being processed

      if (response.status == 200 || response.status == 201) {
        console.log("File uploaded successfully:", response.data);
        fetchFileMetadata();
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Error uploading file!");
    }
  };

  return (
    <div className="App" style={{}}>
      {/* do dome styling of table like add border */}
      <Card
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          maxHeight: "70vh",
          width: "100vw",
          border: "2px solid black",
          borderRadius: "10px",
        }}
      >
        <Typography
          style={{
            marginBottom: "10px",
            marginTop: "10px",
            fontWeight: "bold",
            fontSize: "40px",
            color: "#3f51b5",
            textAlign: "center",
          }}
          variant="h3"
        >
          Candle Stick Data Table
        </Typography>
        <TableContainer>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell align="center">Id</TableCell>
                <TableCell align="center">Name</TableCell>
                <TableCell align="center">Size</TableCell>
                <TableCell align="center">Type</TableCell>
                <TableCell align="center">Created</TableCell>
                <TableCell align="center">View</TableCell>
              </TableRow>
            </TableHead>
            <TableBody style={{ maxHeight: "250px", overflow: "scroll" }}>
              {fileMetadataList.length > 0 ? (
                fileMetadataList.map((row: FileMetadata) => {
                  const date = new Date(row.created_at);
                  return (
                    <TableRow
                      key={row.id}
                      sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                    >
                      <TableCell align="center" component="th" scope="row">
                        {row.id}
                      </TableCell>
                      <TableCell align="center">{row.file_name}</TableCell>
                      <TableCell align="center">{row.file_size}</TableCell>
                      <TableCell align="center">{row.file_type}</TableCell>
                      <TableCell align="center">
                        {date.toLocaleString("en-US", options)}
                      </TableCell>
                      <TableCell align="center">
                        {row.is_valid ? (
                          <button
                            onClick={() => {
                              setIdChart(row.id);
                              setChartView(true);
                            }}
                          >
                            <Typography
                              variant="body1"
                              style={{ color: "green", fontWeight: "bold", fontSize: "15px",  }}
                            >
                              Visualize
                            </Typography>
                          </button>
                        ) : (
                          <Typography variant="body1" style={{ color: "red" }}>
                            Invalid Data
                          </Typography>
                        )}
                      </TableCell>
                    </TableRow>
                  );
                })
              ) : (
                <TableRow>
                  <TableCell sx={{ minWidth: 650 }} colSpan={6} align="center">
                    No data
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Card>
      {chartView && idChart != null && (
        <Card
          style={{
            position: "fixed",
            top: "50%",
            left: "50%",
            width: "1000px",
            height: "500px",
            transform: "translate(-50%, -50%)",
          }}
        >
          <StockMarketChart id={idChart!} />
          <button
            onClick={() => {
              setChartView(false);
              setIdChart(null);
            }}
          >
            Close
          </button>
        </Card>
      )}
      {<WebSocketComponent setIsTableDataValid={() => fetchFileMetadata()} />}
      <Card
        style={{
          width: "95%",
          height: "15vh",
          maxWidth: "600px",
          marginBottom: "2px",
          margin: "10px",
          padding: "20px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          position: "fixed",
          bottom: "20px",
          left: "50%",
          transform: "translateX(-50%)",
          borderRadius: "10px",
          zIndex: 1000,
        }}
      >
        {loading && (
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              marginBottom: "20px",
            }}
          >
            <CircularProgress />
            <Typography variant="body1" style={{ marginTop: "10px" }}>
              File is processing...
            </Typography>
          </div>
        )}

        <Typography
          variant="h5"
          style={{ marginBottom: "15px", fontWeight: "bold", color: "#3f51b5" }}
        >
          Upload JSON File
        </Typography>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            width: "100%",
          }}
        >
          <input
            type="file"
            accept=".json"
            onChange={handleFileChange}
            style={{ marginBottom: "15px", width: "100%" }}
          />
          <button
            onClick={handleUpload}
            style={{
              backgroundColor: "#3f51b5",
              height: "5vh",
              color: "white",
              padding: "10px 10px",
              borderRadius: "5px",
              fontWeight: "bold",
              cursor: "pointer",
              border: "none",
              width: "100%",
              maxWidth: "200px",
            }}
          >
            Upload
          </button>
        </div>
      </Card>
    </div>
  );
}
export default App;
