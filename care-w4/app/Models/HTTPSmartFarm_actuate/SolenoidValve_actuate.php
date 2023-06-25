<?php

namespace App\Models\HTTPSmartFarm_actuate;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class SolenoidValve_actuate extends Model
{
    use HasFactory;

    protected $connection = 'HTTPSmartFarm_actuate';
    protected $table = "solenoidValve_actuate";
    protected $primaryKey = "_id";

    protected $fillable = [
        'value', 
        'type', 
        'unit', 
        'time',
    ];
}
