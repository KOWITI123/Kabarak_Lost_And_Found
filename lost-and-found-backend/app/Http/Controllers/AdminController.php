<?php

namespace App\Http\Controllers;

use App\Http\Requests\UpdateClaimRequest;
use App\Http\Resources\ClaimResource;
use App\Models\Claim;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class AdminController extends Controller
{
    public function getClaims()
    {
        $claims = Claim::where('status', 'Pending')->with('item')->get();
        return ClaimResource::collection($claims);
    }

    public function updateClaim(UpdateClaimRequest $request, $id)
    {
        $claim = Claim::findOrFail($id);
        $status = $request->status;

        if ($status === 'Approved') {
            $claim->status = 'Approved';
            $claim->save();

            $item = $claim->item;
            if ($item) {
                $item->status = 'Returned';
                $item->save();
            }
        } else {
            $claim->status = 'Rejected';
            $claim->save();
        }

        return response()->json([
            'message' => 'Claim updated successfully',
            'claim' => new ClaimResource($claim)
        ]);
    }

    public function getStats()
    {
        $stats = DB::table('daily_stats')->orderBy('id', 'desc')->first();
        return response()->json($stats);
    }
}
