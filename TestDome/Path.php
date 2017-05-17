<?php
class Path
{
    public $currentPath;

    function __construct($path)
    {
        $this->currentPath = $path;
    }

    public function cd($newPath)
    {
    	$currentPath = explode('/', $this->currentPath);
    	$operations = explode('/', $newPath);

    	foreach ($operations as $operation) {
    		if ($operation === '..') {
    			array_pop($currentPath);
    		}
    		else {
    			array_push($currentPath, $operation);
    		}
    	}

    	$this->currentPath = implode('/', $currentPath);
    }
}

$path = new Path('/a/b/c/d');
$path->cd('../x');
echo $path->currentPath;
