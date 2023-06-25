<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\HTTPSmartFarm_actuate\SolenoidValve_actuate;
use App\Models\HTTPSmartFarm\SolenoidValve;
use App\Models\HTTPAQM_actuate\FilterFanSensor_actuate;
use App\Models\HTTPAQM_actuate\WindowSensor_actuate;

use App\Models\HTTPAQM\FilterFanSensor;
use App\Models\HTTPAQM\WindowSensor;

use MongoDB\BSON\UTCDateTime;

use Carbon\Carbon;

class Chart extends Controller
{
    function chart($database, $folder, $start_date = null, $end_date = null) 
    {
        $namespace = "\App\Models\\$database\\$folder";

        try {
            $models = new $namespace;  
        } catch (\Throwable $th) {
            abort(404);
        } 
        
        if($start_date) {
            $models = $models->where('time', '>=', new UTCDateTime(Carbon::parse($start_date))) ;
    
            if ($end_date) {
                $models = $models->where('time', '<=', new UTCDateTime(Carbon::parse($end_date)));
            }
        } else {
            $models = $models->where('time', '>=', new UTCDateTime(now()->subDays(30)));
        }
    
        $models = $models->get();
        
        $result = [];
        $chartData = [];
        $labels = [];
    
        foreach ($models as $model) {
            $labels[] =  $model->time->toDateTime()->format('m-d-y H:i:s');
            $chartData[] = $model->value;
        }
       
        $result = (object) [    
            'type' => 'line',
            'labels' => (array) $labels,
            'datasets' => (array) [
                (object) [
                    'label' => $folder,
                    'data' => $chartData,
                    "fill" =>  true,
                    "borderColor" => "#50C878",
                    "tension" => 0.1,
                    "backgroundColor" => "rgba(80,200,120,0.5)",
                    "cornerRadius" => 10
                ]
            ]
        ];
        
        $databases = $this->databases();
        $folders = $databases[$database];
        $result =  json_encode($result);
    
        $start_date = $start_date ? Carbon::parse($start_date)->format('m-d-Y') : null;
        $end_date = $end_date ? Carbon::parse($end_date)->format('m-d-Y') : null;

        $solenoidValve_actuate = null;
        $filterFanSensor_actuate = null;
        $windowSensor_actuate = null;
        
        if ($database === "HTTPSmartFarm") {
            $solenoidValve_actuate = SolenoidValve::orderBy('_id', 'desc')->first();
        }

        if ($database === "HTTPAQM") {
            $filterFanSensor_actuate = FilterFanSensor::orderBy('_id', 'desc')->first();
            $windowSensor_actuate = WindowSensor::orderBy('_id', 'desc')->first();
        }
        
        $allDatabases = $this->databases();

        return view('chart', compact('result', 'database', 'folder', 'folders', 'start_date', 'end_date', 'solenoidValve_actuate', 'filterFanSensor_actuate', 'windowSensor_actuate', 'allDatabases'));
    }

    function realtimeChart($database, $folder, $start_date = null, $end_date = null) 
    {
        $namespace = "\App\Models\\$database\\$folder";
    
        try {
            $models = new $namespace;  
        } catch (\Throwable $th) {
            abort(404);
        } 
        
     
        $model = $models->orderBy('_id', 'desc')->first();
        
        $result = (object) [
            'label' => now()->format('H:i:s'),
            'data' => 0
        ];

        if($model) {
            $result = (object) [    
                'label' =>  now()->format('H:i:s'),
                'data' => $model->value,
            ];
        }

        return response()->json($result);
    }
    function home()
    {
        $databases = $this->databases();

        return view('home', compact('databases'));
    }

    function timeRange(Request $request) {
        
        $start = Carbon::parse($request->start)->format('Y-m-d');
        $end = Carbon::parse($request->end)->format('Y-m-d');
    

        return redirect("/{$request->database}/{$request->folder}/{$start}/{$end}");
    }

    public static function databases() {
        return [

            'oneM2M_HTTP_AQM' => [
                "PM2_5" ,
            ],
            'oneM2M_MQTT_AQM' => [
                "H2S" ,
                "Humidity" ,
                "PM10" ,
                "PM2_5" ,
                "Temperature" ,
            ],
            'oneM2M_MQTT_SmartFarm' => [
                "ElecConductivity" ,
                "Env_Temp",
                "Humidity" ,
                "Sol_Temp" ,
                "Temperature" ,
                "WaterLevel" ,
                "pH" ,
            ],
            'HTTPSmartFarm' => [
                "ECmeter",
                "dht22Humi",
                "dht22Temp",
                "flowMeter",
                "motorSensor",
                "overflowSensor",
                "pHsensor",
                "solenoidValve",
                "waterLevel",
            ],
            'HTTPAQM' => [
                "PM2_5_Indoor" ,
                "PM2_5_Outdoor" ,
                "Dht22Humi" ,
                "Dht22Temp" ,
                "FilterFanSensor" ,
                "WindowSensor" ,
            ]
            /*  
            'Nodes' => [
                "Nodes"
            ]
            */
        ];
    }
}
