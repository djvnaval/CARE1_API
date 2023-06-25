<?php

namespace App\Models\HTTPAQM;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class Dht22Temp extends Model
{
    use HasFactory;
    protected $connection = 'HTTPAQM';
    protected $table = "dht22Temp";
    protected $primaryKey = "_id";
}
