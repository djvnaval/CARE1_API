<?php

namespace App\Models\HTTPSmartFarm;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class MotorSensor extends Model
{
    use HasFactory;
    protected $connection = 'HTTPSmartFarm';
    protected $table = "motorSensor";
    protected $primaryKey = "_id";
}
