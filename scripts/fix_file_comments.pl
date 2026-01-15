#!/usr/bin/perl


use File::Find;
use File::Basename;

find(
    {
        wanted => \&findfiles,
    },
    'src'
);

find(
    {
        wanted => \&findfiles,
    },
    'tests'
);




sub findfiles
{

    $header = <<EOH;
/*
 * Synth Template
 *
 * Based on SideQuest Starting Point by baconpaul, adopted by David303ttl.
 *
 * Copyright 2024-2025, Paul Walker and contributors.
 * Copyright 2026, Pawel Marczak
 *
 * This source repo is released under the MIT license, but has
 * GPL3 dependencies, as such the combined work will be
 * released under GPL3.
 *
 * The source code and license are at https://github.com/David303ttl/synth-template
 * Original template at https://github.com/baconpaul/sidequest-startingpoint
 */
EOH

    $f = $File::Find::name;
    if ($f =~ m/\.h$/ or $f =~ m/.cpp$/)
    {
        #To search the files inside the directories
        print "Processing $f\n";

        $q = basename($f);
        print "$q\n";
        open(IN, "<$q") || die "Cant open IN $!";
        open(OUT, "> ${q}.bak") || die "Cant open BAK $!";

        $nonBlank = 0;
        $inComment = 0;
        while(<IN>)
        {
            if ($nonBlank)
            {
                print OUT
            }
            else
            {
                if (m:^\s*/\*:) {
                    $inComment = 1;
                }
                elsif (m:\s*\*/:)
                {
                    print OUT $header;
                    $nonBlank = true;
                    $inComment = false;
                }
                elsif ($inComment)
                {

                }
                elsif (m:^//:)
                {

                }
                else
                {
                    print OUT $header;
                    $nonBlank = true;
                    print OUT;

                }
            }
        }
        close(IN);
        close(OUT);
        system("mv ${q}.bak ${q}");
        system("clang-format -i ${q}");
    }
}
