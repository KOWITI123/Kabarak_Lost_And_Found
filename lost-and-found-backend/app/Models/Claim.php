<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Claim extends Model
{
    protected $table = 'claims';

    public $timestamps = false;

    protected $fillable = [
        'item_id',
        'claimant_name',
        'student_reg_no',
        'status',
    ];

    public function item()
    {
        return $this->belongsTo(Item::class);
    }
}
