<?php

namespace App\Models\HTTPAQM;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class WindowSensor_actuate extends Model
{
    use HasFactory;
    protected $connection = 'HTTPAQM';
    protected $table = "windowSensor_actuate";
    protected $primaryKey = "_id";

    protected $fillable = [
        'value', 
        'type', 
        'unit', 
        'time',
    ];
}
