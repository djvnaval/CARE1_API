<?php

namespace App\Models\HTTPAQM_actuate;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class WindowSensor_actuate extends Model
{
    use HasFactory;
    protected $connection = 'HTTPAQM_actuate';
    protected $table = "windowSensor_actuate";
    protected $primaryKey = "_id";

    protected $fillable = [
        'value', 
        'type', 
        'unit', 
        'time',
    ];
}
