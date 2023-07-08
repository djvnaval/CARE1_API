<?php

namespace App\Http\Controllers\oneM2M_MQTT_AQM;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\oneM2M_MQTT_AQM\FilterFan;

class FilterFanController extends Controller
{
    public function show() 
    {
        $data = FilterFan::orderBy('_id', 'desc')->first();

        return response()->json(compact('data'));
    }
}
