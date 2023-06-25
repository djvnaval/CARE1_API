<?php

namespace App\Models\HTTPAQM;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class FilterFanSensor extends Model
{
    use HasFactory;
    protected $connection = 'HTTPAQM';
    protected $table = "filterFanSensor";
    protected $primaryKey = "_id";
}
