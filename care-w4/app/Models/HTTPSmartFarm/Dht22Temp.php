<?php

namespace App\Models\HTTPSmartFarm;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class Dht22Temp extends Model
{
    use HasFactory;
    protected $connection = 'HTTPSmartFarm';
    protected $table = "dht22Temp";
    protected $primaryKey = "_id";
}
