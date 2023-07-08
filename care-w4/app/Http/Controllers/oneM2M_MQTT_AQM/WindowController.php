<?php

namespace App\Http\Controllers\oneM2M_MQTT_AQM;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\oneM2M_MQTT_AQM\Window;

class WindowController extends Controller
{
    public function show() 
    {
        $data = Window::orderBy('_id', 'desc')->first();

        return response()->json(compact('data'));
    }
}
