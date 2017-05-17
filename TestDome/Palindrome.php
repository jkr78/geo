<?php
class Palindrome
{
    public static function isPalindrome($word)
    {
        for($i = 0; $i < strlen($word); $i++) {
        	$lhs = strtolower($word{$i});
        	$rhs = strtolower(substr($word, -($i + 1), 1));
        	if ($lhs !== $rhs) {
        		return false;
        	}
        }

        return true;
    }
}

echo Palindrome::isPalindrome('Deleveled');