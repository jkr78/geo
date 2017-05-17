<?php
class Thesaurus
{
    private $thesaurus;

    function Thesaurus($thesaurus)
    {
        $this->thesaurus = $thesaurus;
    }

    public function getSynonyms($word)
    {
        $synonyms = array(
            'word' => $word,
            'synonyms' => array(),
        );

        if (array_key_exists($word, $this->thesaurus)) {
            $synonyms['synonyms'] = $this->thesaurus[$word];
        }

        return json_encode($synonyms);
    }
}

$thesaurus = new Thesaurus(
    array 
        (
            "buy" => array("purchase"),
            "big" => array("great", "large")
        )); 

echo $thesaurus->getSynonyms("big");
echo "\n";
echo $thesaurus->getSynonyms("agelast");