<?php

namespace App\Models\HTTPAQM;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class PM2_5_Indoor extends Model
{
    use HasFactory;
    protected $connection = 'HTTPAQM';
    protected $table = "PM2_5_indoor";
    protected $primaryKey = "_id";
}
