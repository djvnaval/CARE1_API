<?php

namespace App\Http\Controllers\HTTPAQM_actuate;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\HTTPAQM_actuate\FilterFanSensor_actuate;

use MongoDB\BSON\UTCDateTime;

class FilterFanSensor_actuateController extends Controller
{
    public function store(Request $request) 
    {
        $latest = FilterFanSensor_actuate::orderBy('_id', 'desc')->first();
        
        $value = $latest->value ? 0 : 1;

        $data = FilterFanSensor_actuate::create([
            'value' => $value, 
            'type' => 'filter fan sensor', 
            'unit' => 'none', 
            'time' => new UTCDateTime(now()),
        ]);

        return response()->json(compact('data'));
    } 
}
