<?php

namespace JsullivanUs\EightQueens;

class QueenBoard
{

    /** @var An integer used as the width and length of the board */
    public function __construct($board_size)
    {
        $this->size = $board_size;

        $this->queens = array_fill(0, $board_size, 0);

        $this->sol_count = 0;
    }

    /** 
     * A recursive generator that yields solutions as arrays of integers.
     *
     * The return value is a reference to an internal array, so if you want
     * to store or modify the array, you need to copy it first.
     */
    public function solutions($column = 0)
    {
        // If this is a valid solution, yield it.
        if ($column == $this->size) {
            $this->sol_count++;
            yield $this->queens;
        }

        // Go through each row in this column, trying to place a queen in it.
        for ($row = 0; $row < $this->size; $row++) {
            if (!$this->under_attack($column, $row)) {
                $this->queens[$column] = $row;
                foreach ($this->solutions($column + 1) as $solution) {
                    yield $this->queens;
                }
            }
        }
    }

    /**
     * Check whether a queen is under attack by any queen in a lesser column.
     */
    protected function under_attack($column, $row)
    {
        /* 
         * For each Lesser Column ($lc) check if the queen can attack us
         * vertically or diagonally.
         */
        for ($lc = 0; $lc < $column; $lc++) {
            $col_diff = $column - $lc;
            if ($this->queens[$lc] == $row - $col_diff ||
                $this->queens[$lc] == $row ||
                $this->queens[$lc] == $row + $col_diff) {
                return true;
            }   
        }
        return false;
    }

    /**
     * Returns the number of solutions we have yielded so far.
     */
    public function solution_count() {
        return $this->sol_count;
    }

    public function print_solution() {
        foreach ($this->queens as $pos) {
            echo(str_repeat("[]", $pos) . "%%" . 
                 str_repeat("[]", $this->size - $pos - 1) . PHP_EOL);
        }
    }
}


$qb = new QueenBoard(8);
foreach($qb->solutions() as $sol) {
    $qb->print_solution();
    echo(PHP_EOL);
}

echo($qb->solution_count() . " solutions" . PHP_EOL);
