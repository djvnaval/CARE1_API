<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class Node extends Model
{
    use HasFactory;
    protected $connection = 'Nodes';
    protected $table = 'Nodes';
    protected $primaryKey = "_id";
}

   
