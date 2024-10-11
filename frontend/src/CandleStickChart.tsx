import React, { useEffect, useRef, useState } from 'react';
import { Chart as ReactChart } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  TimeScale,
  Tooltip,
  Legend,
} from 'chart.js';
import 'chartjs-chart-financial';
import 'chartjs-adapter-date-fns';
import zoomPlugin from 'chartjs-plugin-zoom';
import axios from 'axios';

import { candlestickData } from './candel'; //test json filr


interface SecurityData {
  c: string;
  o: string;
  h: string;
  l: string;
  x:any;
}

ChartJS.register(
  CategoryScale,
  LinearScale,
  TimeScale,
  Tooltip,
  Legend,
  require('chartjs-chart-financial').CandlestickController,
  require('chartjs-chart-financial').CandlestickElement,
  zoomPlugin
);

const StockMarketChart = ({id}:{id :number}) => {
  const [loading, setLoading] = useState<boolean>(true);
  const chartRef = useRef<any>(null);
  const [securityData, setSecurityData]=useState<SecurityData[] | null>();


  useEffect(()=>{
    getSecurityData(id);
  },[id])

  const getSecurityData = async (fileMetadataId: number) => {
    console.log('called');
    try {
        const response = await axios.get(`http://localhost:8000/api/v1/get_security_data?file_metadata_id=${fileMetadataId}`);
        if(response.status==200){
          const formattedData = response.data.map((item:any) =>{
            // console.log(item.x);
            return(
              {
                x: new Date(item.x).getTime(),
              o: item.o,
              h: item.h,
              l: item.l,
              c: item.c
            })
          } );
          // console.log(formattedData);
          setSecurityData(formattedData);
          setLoading(false);
        }
        else{
          setSecurityData(null);
        }
    } catch (error:any) {
        console.error('Error fetching security data:', error);
        alert('error getting the file')
        if(error.response.status==404){
          alert('file not found');
          setSecurityData(null);
          setLoading(true);
    }
  }
};

  const data = {
    datasets: [{
      label: 'Stock Price',
      data: securityData,
      borderColor: 'black',
      backgroundColor: (context: any) => {
        return context.dataset.data[context.dataIndex].c > context.dataset.data[context.dataIndex].o
          ? 'rgba(0, 255, 0, 0.5)'
          : 'rgba(255, 0, 0, 0.5)';
      },
    }],
  };

  const options: any = {
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'month',
        },
        title: {
          display: true,
          text: 'Date',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Price (USD)',
        },
      },
    },
    plugins: {
      tooltip: {
        mode: 'nearest',
        intersect: false,
      },
      zoom: {
        pan: {
          enabled: true,
          mode: 'xy',
        },
        zoom: {
          wheel: {
            enabled: true,
          },
          pinch: {
            enabled: true,
          },
          mode: 'xy',
        },
      },
      legend: {
        display: false,
        position: 'top',
      },
    },
  };

  const handleResetZoom = () => {
    if (chartRef.current) {
      chartRef.current.resetZoom();
    }
  };

  if (loading) return <div>Loading...</div>;
  if(securityData==null) return <div>Data not Found</div>

  return (
    <div>
      {securityData!=null && <ReactChart ref={chartRef} type="candlestick" data={data} options={options as any} />}
      <button onClick={handleResetZoom}>Reset Zoom</button>
    </div>
  );
};

export default StockMarketChart;
