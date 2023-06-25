<?php

namespace App\Models\HTTPAQM;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class WindowSensor extends Model
{
    use HasFactory;
    protected $connection = 'HTTPAQM';
    protected $table = "windowSensor";
    protected $primaryKey = "_id";
}
