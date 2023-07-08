<?php

namespace App\Http\Controllers\oneM2M_MQTT_AQM;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\oneM2M_MQTT_AQM\Window_actuate;

use MongoDB\BSON\UTCDateTime;

class Window_actuateController extends Controller
{
    public function store(Request $request) 
    {
        $latest = Window_actuate::orderBy('_id', 'desc')->first();
        
        $value = $latest->value ? 0 : 1;
        //$value = !$latest->value;

        $data = Window_actuate::create([
            'value' => $value, 
            'type' => 'window', 
            'unit' => 'none', 
            'time' => new UTCDateTime(now()),
        ]);

        return response()->json(compact('data'));
    } 
}
