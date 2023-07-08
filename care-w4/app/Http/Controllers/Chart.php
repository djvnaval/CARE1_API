<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use App\Models\HTTPSmartFarm\SolenoidValve;
use App\Models\HTTPAQM\FilterFanSensor;
use App\Models\HTTPAQM\WindowSensor;
use App\Models\oneM2M_MQTT_AQM\FilterFan;
use App\Models\oneM2M_MQTT_AQM\Window;

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
            $models = $models->where('time', '>=', new UTCDateTime(Carbon::parse($start_date)));
 
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
        $unit = '';
    
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
                    "borderColor" => "#fffaa8",
                    "borderWidth" => 3,
                    "tension" => 0.1,
                    "backgroundColor" => "transparent",
                    "cornerRadius" => 1
                ]
            ]
        ];  
        
        $chartData = !$chartData ? [0] : $chartData;

        $min = min($chartData);
        $max = max($chartData);
        $average = array_sum($chartData)/count($chartData);

        if ($chartData !== [0]){
            $unit = $models[0]->unit && $models[0]->unit != 'none' ? $models[0]->unit : '';
        }
        $databases = $this->databases();
        $folders = $databases[$database];
        $result =  json_encode($result);
    
        $start_date = $start_date ? Carbon::parse($start_date)->format('m-d-Y H:i:s') : null;
        $end_date = $end_date ? Carbon::parse($end_date)->format('m-d-Y H:i:s') : null;
        
        $solenoidValve_actuate = null;
        $filterFanSensor_actuate = null;
        $windowSensor_actuate = null;
        $FilterFan_actuate = null;
        $Window_actuate = null;
        
        if ($database === "HTTPSmartFarm") {
            $solenoidValve_actuate = SolenoidValve::orderBy('_id', 'desc')->first();
        }

        if ($database === "HTTPAQM") {
            $filterFanSensor_actuate = FilterFanSensor::orderBy('_id', 'desc')->first();
            $windowSensor_actuate = WindowSensor::orderBy('_id', 'desc')->first();
        }
        
        if ($database === "oneM2M_MQTT_AQM") {
            $FilterFan_actuate = FilterFan::orderBy('_id', 'desc')->first();
            $Window_actuate = Window::orderBy('_id', 'desc')->first();
        }

        $allDatabases = $this->databases();

        return view('chart', compact('result', 'database', 'folder', 'folders', 'start_date', 'end_date', 'solenoidValve_actuate', 'filterFanSensor_actuate', 'windowSensor_actuate', 'FilterFan_actuate', 'Window_actuate', 'allDatabases', 'min', 'max', 'average', 'unit'));
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

    function timeRange(Request $request) 
    {    
        $dateTimes = explode(' - ', $request->datetimes);
        $start = Carbon::parse($dateTimes[0])->format('Y-m-d H:i:s');
        $end = Carbon::parse($dateTimes[1])->format('Y-m-d H:i:s');
        
        return redirect("/{$request->database}/{$request->folder}/{$start}/{$end}");
    }

    public static function databases() 
    {
        return [
            'oneM2M_MQTT_AQM' => [ 
                "Humidity" => ["Relative humidity outdoors",[60,80,100]],
                "Humidity_In" => ["Relative humidity indoors",[60,80,100]],
                "PM2_5_Out" => ["Fine particulate matter in the air that are two and one half microns or less in width",[60,80,300]],
                "PM2_5_In" => ["Fine particulate matter in the air that are two and one half microns or less in width",[35,80,200]],
                "Temperature" => ["Relative temperature outdoors",[32,35,45]], 
                "Temperature_In" => ["Relative temperature indoors",[32,35,45]], 
                "FilterFan" => ["Signals whether filter fans are turned on or off",[1,2,3]],  
                "FilterFan_actuate" => ["Signals whether filter fans are turned on or off",[1,2,3]], 
                "Window" => ["Signals whether the window is open or close",[1,2,3]], 
                "Window_actuate" => ["Signals whether the window is open or close",[1,2,3]], 
                "H2S" => ["Hydrogen sulfide is a higly toxic gas that is estimated to remain in the atmosphere for about 18 hours",[0,20,50]],
                "PM10" => ["Particulate matter in the air that are ten microns or less in width",[100,200,300]],
                "PM2_5" => ["Fine particulate matter in the air that are two and one half microns or less in width",[100,200,300]],
            ],
            'oneM2M_MQTT_SmartFarm' => [
                "ElecConductivity" => ["Electrical Conductivity measures how much dissolved substances, chemicals, and minerals are present in the water",[100,200,300]],
                "Env_Temp"=> ["Relative Environment Temperature",[32,35,45]],
                "Humidity" => ["Relative Humidity",[60,80,100]],
                "Sol_Temp" => ["Relative Soil Temperature",[100,200,300]],
                "Temperature" => ["Relative Temperature",[100,200,300]],
                "WaterLevel" => ["Measures the water left in the tank",[100,200,300]],
                "pH" => ["PH measures how acidic/basic the water is",[100,200,300]],
            ],
            'HTTPSmartFarm' => [
                "ECmeter" => ["Electrical Conductivity measures how much dissolved substances, chemicals, and minerals are present in the water",[2,3,4]],
                "dht22Humi" => ["Relative Humidity",[50,70,90]],
                "dht22Temp" => ["Relative Temperature",[100,200,300]],
                "waterLevel" => ["Measures the water left in the tank",[50,55,60]],
                "solenoidValve" => ["Description",[100,200,300]],
                "solenoidValve_actuate" => ["Description",[100,200,300]],
                "pHsensor" => ["pH measures how acidic/basic the water is",[7.5,8,9]],
                "flowMeter" => ["Description",[100,200,300]],
                "motorSensor" => ["Description",[100,200,300]],
                "overflowSensor" => ["Check if the tank is overflowing",[100,200,300]],
            ],
            'HTTPAQM' => [
                "PM2_5_Indoor" => ["Fine particulate matter in the air indoors that are two and one half microns or less in width",[35,80,200]],
                "PM2_5_Outdoor" => ["Fine particulate matter in the air outdoors that are two and one half microns or less in width",[60,80,300]],
                "Dht22Humi" => ["Relative Humidity",[60,80,100]],
                "Dht22Temp" => ["Relative Temperature",[32,35,45]], 
                "FilterFanSensor" => ["Signals whether filter fans are turned on or off",[1,2,3]], 
                "WindowSensor" => ["Signals whether the window is open or close",[1,2,3]], 
                "FilterFanSensor_actuate" => ["Signals whether filter fans are turned on or off",[1,2,3]], 
                "WindowSensor_actuate" => ["Signals whether the window is open or close",[1,2,3]], 
            ],
            'oneM2M_HTTP_AQM' => [
                "PM2_5" => ["Fine particulate matter in the air that are two and one half microns or less in width",[100,200,300]]
            ]
        ];
    }
}
