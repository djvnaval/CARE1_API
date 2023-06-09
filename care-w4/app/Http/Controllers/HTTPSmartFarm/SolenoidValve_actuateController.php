<?php

namespace App\Http\Controllers\HTTPSmartFarm;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\HTTPSmartFarm\SolenoidValve_actuate;

use MongoDB\BSON\UTCDateTime;

class SolenoidValve_actuateController extends Controller
{
    public function store(Request $request) 
    {
        $latest = SolenoidValve_actuate::orderBy('_id', 'desc')->first();
        
        $value = $latest->value ? 0 : 1;
        //$value = !$latest->value;

        $data = SolenoidValve_actuate::create([
            'value' => $value, 
            'type' => 'solenoid valve', 
            'unit' => 'none', 
            'time' => new UTCDateTime(now()),
        ]);

        return response()->json(compact('data'));
    } 
}
