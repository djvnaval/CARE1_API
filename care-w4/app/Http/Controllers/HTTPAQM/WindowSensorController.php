<?php

namespace App\Http\Controllers\HTTPAQM;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\HTTPAQM\WindowSensor;

class WindowSensorController extends Controller
{
    public function show() 
    {
        $data = WindowSensor::orderBy('_id', 'desc')->first();

        return response()->json(compact('data'));
    }
}
