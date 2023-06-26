<?php

namespace App\Models\HTTPSmartFarm;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class OverflowSensor extends Model
{
    use HasFactory;
    protected $connection = 'HTTPSmartFarm';
    protected $table = "overflowSensor";
    protected $primaryKey = "_id";
}
