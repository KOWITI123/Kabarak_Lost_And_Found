<?php

namespace App\Http\Controllers;

use App\Models\Item;
use Illuminate\Http\Request;

class WhatsAppController extends Controller
{
    public function handleWebhook(Request $request)
    {
        $body = $request->input('Body');

        if (empty($body)) {
            return response()->json(['message' => 'No body provided'], 400);
        }

        // Pattern: "Found [Item] at [Location]"
        if (preg_match('/Found (.+) at (.+)/i', $body, $matches)) {
            $itemName = trim($matches[1]);
            $location = trim($matches[2]);

            $item = Item::create([
                'item_name' => $itemName,
                'description' => 'Reported via WhatsApp',
                'location_found' => $location,
                'status' => 'Found',
                'date_reported' => now(),
            ]);

            return response()->json(['message' => 'Item reported successfully', 'item' => $item]);
        }

        return response()->json(['message' => 'Pattern not matched'], 200);
    }
}
