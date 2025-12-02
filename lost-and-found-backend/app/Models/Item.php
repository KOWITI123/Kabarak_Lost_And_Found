<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Item extends Model
{
    protected $table = 'items';

    public $timestamps = false;

    protected $fillable = [
        'item_name',
        'description',
        'location_found',
        'status',
        'date_reported',
    ];

    protected $casts = [
        'date_reported' => 'datetime',
    ];

    public function claims()
    {
        return $this->hasMany(Claim::class);
    }
}
