<?php

namespace App\Http\Controllers\oneM2M_MQTT_AQM;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\oneM2M_MQTT_AQM\FilterFan_actuate;

use MongoDB\BSON\UTCDateTime;

class FilterFan_actuateController extends Controller
{
    public function store(Request $request) 
    {
        $latest = FilterFan_actuate::orderBy('_id', 'desc')->first();
        
        $value = $latest->value ? 0 : 1;
        //$value = !$latest->value ? 1 : 0;
        /*
        $value = null;
        if ($latest->value == 1){
            $value = 0;
        }elseif ($latest->value == 0){
            $value = 1;
        }*/

        $data = FilterFan_actuate::create([
            'value' => $value, 
            'type' => 'filter fan', 
            'unit' => 'none', 
            'time' => new UTCDateTime(now()),
        ]);

        return response()->json(compact('data'));
    } 
}

