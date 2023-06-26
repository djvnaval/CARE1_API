<?php

namespace App\Http\Controllers\HTTPAQM;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\HTTPAQM\FilterFanSensor;

class FilterFanSensorController extends Controller
{
    public function show() 
    {
        $data = FilterFanSensor::orderBy('_id', 'desc')->first();

        return response()->json(compact('data'));
    }
}
