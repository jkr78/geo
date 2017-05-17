<?php
class FileOwners
{
    public static function groupByOwners($files)
    {
    	$groupedByOwner = array();
        foreach ($files as $file => $owner) {
        	if (!array_key_exists($owner, $groupedByOwner)) {
        		$groupedByOwner[$owner] = array();
        	}

        	$groupedByOwner[$owner][] = $file;
        }

        return $groupedByOwner;
    }
}

$files = array
(
    "Input.txt" => "Randy",
    "Code.py" => "Stan",
    "Output.txt" => "Randy"
);
var_dump(FileOwners::groupByOwners($files));