<?php

namespace App\Http\Controllers\HTTPSmartFarm;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\HTTPSmartFarm\SolenoidValve;

class SolenoidValveController extends Controller
{
    public function show() 
    {
        $data = SolenoidValve::orderBy('_id', 'desc')->first();

        return response()->json(compact('data'));
    }
}

