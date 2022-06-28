import Chart from "react-google-charts";


export default function ChartGraph({List, color, title}){

    return(
        <div style={{ alignContent: "center", width: '95%', margin:'auto'}}>
            <h3>Plot</h3>
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
                    innerWidth:'80%',
                    width: '70%'
                    },
            hAxis: {
                title: 'Time',
            },
            backgroundColor: {
                fill: color,//'#fbf6a7','#c39ea0'
                fillOpacity: 0.8},
            color:"white",
            vAxis: {
                title: title,
            }
            }}
            />
        </div>

    )
}