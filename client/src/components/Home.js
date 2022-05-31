// import { Home } from '@mui/icons-material';
import React, { useState, useEffect } from 'react';
import Chart from "react-google-charts";
import axios from 'axios'

export default function HomePage() {

    let valueList=[];
    const [file, setFile] = useState();
    const [output, setoutput] = useState();
    const [outputArray, setoutputArray] = useState([]);
    const [getMessage, setGetMessage] = useState({})
    const [getMessage1, setGetMessage1] = useState({})

    const [List,setList]=useState([]);

    const fileReader = new FileReader();

    const handleOnChange = (e) => {
        setFile(e.target.files[0]);
        const data = new FormData();

        data.append('file', e.target.files[0]);
        // data.append('filename', this.fileName.value);

        fetch('http://localhost:5000/autoarima', {
        method: 'POST',
        body: data,
        }).then((response) => {
        response.json().then((body) => {
            console.log("file went bruh")
        });
        });

        
    };

    useEffect(()=>{
        axios.get('http://127.0.0.1:5000/time').then(response => {
          console.log("SUCCESS", response)
          setGetMessage(response)
        }).catch(error => {
          console.log(error)
        })

        axios.get('http://127.0.0.1:5000/hello').then(response => {
          console.log("SUCCESS", response)
          setGetMessage1(response)
        }).catch(error => {
          console.log(error)
        })
    
      }, [])

    const handleOnSubmit = (e) => {
        e.preventDefault();

        if (file) {
            fileReader.onload = function (event) {
                const csvOutput = event.target.result;
                setoutput(csvOutput.split('\n'));
                setoutputArray(csvOutput.split('\n'));

            };

            // setoutputArray(output);
            fileReader.readAsText(file);

        }
    };

    const showCSV = (e) => {
        e.preventDefault();
        console.log(typeof(output))

        for (let i = 0; i < output.length; i++) {
            const ele = outputArray[i];
            console.log(ele);
        }
        // console.log(output)
        outputArray.map((record)=>(valueList.push([record.split(',')[0], record.split(',')[1]])));
        valueList.unshift([{ type: 'string', label: 'Time' },{label:'Storage Consumption',type:'number'}])
        setList(valueList);
        console.log(List)

    }

    const showState = (e) => {
        e.preventDefault();
        // for (let i = 0; i < output.length; i++) {
        //     const ele = output[i];
        //     console.log(ele);
        // }
        console.log(List);

    }

    const sendCSV = (e) => {
        e.preventDefault();

        // axios.post('http://127.0.0.1:5000/autoarima').then(response => {
        //   console.log("SUCCESS", response)
        //   setGetMessage(response)
        // }).catch(error => {
        //   console.log(error)
        // })
        let file1 = file;
        const formData = new FormData();

        formData.append("file", file1);

        axios.post('http://127.0.0.1:5000/autoarima', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
        } )
          .then(function (response) {
            console.log(response);
          })
          .catch(function (error) {
            console.log(error);
          });
    }


    return (
        <div>
          

        <div style={{ textAlign: "center" }}>
            <h1>Current usage 1 </h1>
            <div>{getMessage.status === 200 ? 
                <h3>{getMessage.data.message}</h3>
                :
                <h3>LOADING</h3>}
            </div>
            <div>{getMessage1.status === 200 ? 
                <h3>{getMessage1.data.message}</h3>
                :
                <h3>LOADING</h3>}
            </div>
            <form>
                <input
                    type={"file"}
                    id={"csvFileInput"}
                    accept={".csv"}
                    onChange={handleOnChange}
                />

                <button
                    onClick={(e) => {
                        handleOnSubmit(e);
                    }}
                >
                    IMPORT CSV
                </button>

                &nbsp;
                <button
                    onClick={(e) => {
                        showCSV(e);
                    }}
                >
                    Plot
                </button>

                <button
                    onClick={(e) => {
                        sendCSV(e);
                    }}
                >
                    Send file
                </button>


                

            </form>
        </div>
        
        <br/>
        <div style={{ alignContent: "center" }}>
            {List.length!=0?
                <Chart
                width={'100%'}
                height={'800px'}
                chartType="LineChart"
                loader={<div>Storage consumption Chart</div>}
                data={
                List
                }
                
                options={{
                    chartArea: {                        
                        innerWidth:'90%',
                        width: '90%'
                      },
                hAxis: {
                    title: 'Time',
                },
                backgroundColor: {
                    fill: '#c39ea0',//'#fbf6a7',
                    fillOpacity: 0.8},
                color:"white",
                vAxis: {
                    title: 'Storage consumption (in MB)',
                }
                }}
                />:<span></span>}
        </div>


          
        </div>
      );
}