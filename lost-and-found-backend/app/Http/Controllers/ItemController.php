<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreClaimRequest;
use App\Http\Requests\StoreItemRequest;
use App\Http\Resources\ClaimResource;
use App\Http\Resources\ItemResource;
use App\Models\Claim;
use App\Models\Item;
use Illuminate\Http\Request;

class ItemController extends Controller
{
    public function index(Request $request)
    {
        $query = Item::where('status', '!=', 'Returned');

        if ($request->has('location_found')) {
            $query->where('location_found', $request->location_found);
        }

        return ItemResource::collection($query->get());
    }

    public function store(StoreItemRequest $request)
    {
        $validated = $request->validated();

        // Set date_reported to now if not provided
        $validated['date_reported'] = now();

        $item = Item::create($validated);

        return new ItemResource($item);
    }

    public function storeClaim(StoreClaimRequest $request)
    {
        $validated = $request->validated();

        $claim = Claim::create([
            'item_id' => $validated['item_id'],
            'claimant_name' => $validated['claimant_name'],
            'student_reg_no' => $validated['student_reg_no'],
            'status' => 'Pending',
        ]);

        return response()->json([
            'message' => 'Claim submitted successfully',
            'claim' => new ClaimResource($claim)
        ], 201);
    }
}
