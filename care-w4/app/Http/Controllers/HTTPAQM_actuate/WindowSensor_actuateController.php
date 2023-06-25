<?php

namespace App\Http\Controllers\HTTPAQM_actuate;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\HTTPAQM_actuate\WindowSensor_actuate;

use MongoDB\BSON\UTCDateTime;

class WindowSensor_actuateController extends Controller
{
    public function store(Request $request) 
    {
        $latest = WindowSensor_actuate::orderBy('_id', 'desc')->first();
        
        $value = $latest->value ? 0 : 1;

        $data = WindowSensor_actuate::create([
            'value' => $value, 
            'type' => 'window sensor', 
            'unit' => 'none', 
            'time' => new UTCDateTime(now()),
        ]);

        return response()->json(compact('data'));
    } 
}
