<?php

namespace App\Http\Controllers\HTTPSmartFarm_actuate;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\HTTPSmartFarm_actuate\SolenoidValve_actuate;

use MongoDB\BSON\UTCDateTime;

class SolenoidValve_actuateController extends Controller
{
    public function store(Request $request) 
    {
        $latest = SolenoidValve_actuate::orderBy('_id', 'desc')->first();
        
        $value = $latest->value ? 0 : 1;

        $data = SolenoidValve_actuate::create([
            'value' => $value, 
            'type' => 'solenoid valve', 
            'unit' => 'none', 
            'time' => new UTCDateTime(now()),
        ]);

        return response()->json(compact('data'));
    } 
}
