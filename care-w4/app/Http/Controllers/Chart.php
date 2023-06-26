<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use App\Models\HTTPSmartFarm\SolenoidValve;
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
                    "borderColor" => "#50C878",
                    "borderWidth" => 4,
                    "tension" => 0.5,
                    "backgroundColor" => "rgba(80,200,120,0.4)",
                    "cornerRadius" => 15
                ]
            ]
        ];
        
        //$chartData = $chartData ?? [0];
        $chartData = is_null($chartData) || empty($chartData) ? [0] : $chartData;

        $min = min($chartData);
        $max = max($chartData);
        $average = array_sum($chartData)/count($chartData);

        if ($chartData !== [0]){
            $unit = $models[0]->unit && $models[0]->unit != 'none' ? $models[0]->unit : '';
        }
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

        return view('chart', compact('result', 'database', 'folder', 'folders', 'start_date', 'end_date', 'solenoidValve_actuate', 'filterFanSensor_actuate', 'windowSensor_actuate', 'allDatabases', 'min', 'max', 'average', 'unit'));
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
        $start = Carbon::parse($request->start)->format('Y-m-d');
        $end = Carbon::parse($request->end)->format('Y-m-d');

        return redirect("/{$request->database}/{$request->folder}/{$start}/{$end}");
    }

    public static function databases() 
    {
        return [
            'oneM2M_HTTP_AQM' => [
                "PM2_5" => ["Fine particulate matter in the air that are two and one half microns or less in width",[100,200,300]]
            ],
            'oneM2M_MQTT_AQM' => [
                "H2S" => ["Hydrogen sulfide is a higly toxic gas that is estimated to remain in the atmosphere for about 18 hours",[100,200,300]], 
                "Humidity" => ["Relative Humidity",[100,200,300]],
                "PM10" => ["Particulate matter in the air that are ten microns or less in width",[100,200,300]],
                "PM2_5" => ["Fine particulate matter in the air that are two and one half microns or less in width",[100,200,300]],
                "Temperature" => ["Relative Temperature",[100,200,300]], 
            ],
            'oneM2M_MQTT_SmartFarm' => [
                "ElecConductivity" => ["Electrical Conductivity measures how much dissolved substances, chemicals, and minerals are present in the water",[100,200,300]],
                "Env_Temp"=> ["Relative Environment Temperature",[100,200,300]],
                "Humidity" => ["Relative Humidity",[100,200,300]],
                "Sol_Temp" => ["Relative Soil Temperature",[100,200,300]],
                "Temperature" => ["Relative Temperature",[100,200,300]],
                "WaterLevel" => ["Measures the water left in the tank",[100,200,300]],
                "pH" => ["PH measures how acidic/basic the water is",[100,200,300]],
            ],
            'HTTPSmartFarm' => [
                "ECmeter" => ["Electrical Conductivity measures how much dissolved substances, chemicals, and minerals are present in the water",[2,3,4]],
                "dht22Humi" => ["Relative Humidity",[50,70,90]],
                "dht22Temp" => ["Relative Temperature",[100,200,300]],
                "flowMeter" => ["Description",[100,200,300]],
                "motorSensor" => ["Description",[100,200,300]],
                "overflowSensor" => ["Description",[100,200,300]],
                "pHsensor" => ["Description",[100,200,300]],
                "solenoidValve" => ["Description",[100,200,300]],
                "solenoidValve_actuate" => ["Description",[100,200,300]],
                "waterLevel" => ["Measures the water left in the tank",[50,55,60]],
            ],
            'HTTPAQM' => [
                "PM2_5_Indoor" => ["Fine particulate matter in the air indoors that are two and one half microns or less in width",[100,300,400]],
                "PM2_5_Outdoor" => ["Fine particulate matter in the air outdoors that are two and one half microns or less in width",[100,300,400]],
                "Dht22Humi" => ["Relative Humidity",[100,200,300]],
                "Dht22Temp" => ["Relative Temperature",[100,200,300]], 
                "FilterFanSensor" => ["Description",[100,200,300]], 
                "WindowSensor" => ["Description",[100,200,300]], 
                "FilterFanSensor_actuate" => ["Description",[100,200,300]], 
                "WindowSensor_actuate" => ["Description",[100,200,300]], 
            ]
        ];
    }
}
