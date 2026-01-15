#!/usr/bin/perl

#
# fix_namespace.pl - Universal namespace migration tool
#
# This script detects the current namespace(s) used in the project and converts them
# to new namespaces specified by the user.
#
# Usage: perl scripts/fix_namespace.pl [new_ns1] [new_ns2]
#
# Example: perl scripts/fix_namespace.pl yourname yourproject
#          (changes david303ttl::synthtemplate to yourname::yourproject)
#

use File::Find;
use File::Basename;

# Function to detect current namespaces from source files
sub detect_current_namespaces
{
    my @files_to_check = (
        'src/configuration.h',
        'src/engine/engine.h',
        'src/engine/patch.h',
        'src/engine/voice.h'
    );

    foreach my $file (@files_to_check) {
        if (-e $file) {
            open(FH, "<$file") or next;
            my @ns_stack = ();
            while (my $line = <FH>) {
                # Look for namespace declarations like: namespace foo {
                if ($line =~ /namespace\s+(\w+)\s*\{/) {
                    push @ns_stack, $1;
                    # If we have 2 namespaces, we found our pattern
                    if (@ns_stack >= 2) {
                        close(FH);
                        return ($ns_stack[0], $ns_stack[1]);
                    }
                }
                # Look for namespace reference like foo::bar::
                if ($line =~ /(\w+)::(\w+)::/) {
                    close(FH);
                    return ($1, $2);
                }
            }
            close(FH);
        }
    }
    return (undef, undef);  # Not found
}

# Detect current namespaces by scanning source files
($old_ns1, $old_ns2) = detect_current_namespaces();

if ($old_ns1 && $old_ns2) {
    print "Detected current namespaces: '$old_ns1' :: '$old_ns2'\n";
} else {
    print "Could not detect current namespaces.\n";
    print "Enter first namespace (e.g., yourname): ";
    $old_ns1 = <STDIN>;
    chomp $old_ns1;
    print "Enter second namespace (e.g., yourproject): ";
    $old_ns2 = <STDIN>;
    chomp $old_ns2;
}

# Get new namespaces from command line arguments, or prompt for them
if (@ARGV >= 2) {
    $new_ns1 = $ARGV[0];
    $new_ns2 = $ARGV[1];
} elsif (@ARGV == 1) {
    $new_ns1 = $ARGV[0];
    print "Enter second new namespace (current: '$old_ns2', press Enter to keep): ";
    $input = <STDIN>;
    chomp $input;
    $new_ns2 = $input || $old_ns2;  # Keep old if Enter pressed
} else {
    print "Enter first new namespace (current: '$old_ns1'): ";
    $new_ns1 = <STDIN>;
    chomp $new_ns1;
    print "Enter second new namespace (current: '$old_ns2', press Enter to keep): ";
    $input = <STDIN>;
    chomp $input;
    $new_ns2 = $input || $old_ns2;  # Keep old if Enter pressed
}

# Trim whitespace
$old_ns1 =~ s/^\s+|\s+$//g;
$old_ns2 =~ s/^\s+|\s+$//g;
$new_ns1 =~ s/^\s+|\s+$//g;
$new_ns2 =~ s/^\s+|\s+$//g;

if ($old_ns1 eq $new_ns1 && $old_ns2 eq $new_ns2) {
    print "Error: Old and new namespaces are the same. Nothing to do.\n";
    exit(1);
}

print "Migrating from '$old_ns1::$old_ns2' to '$new_ns1::$new_ns2'...\n";
print "(Changing: $old_ns1 -> $new_ns1, $old_ns2 -> $new_ns2)\n\n";

# Track files modified
$files_modified = 0;

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

print "\n=== Migration complete ===\n";
print "Total files modified: $files_modified\n";
print "\nRemember to:\n";
print "1. Review the changes with git diff\n";
print "2. Run cmake --build build --config Release\n\n";

sub findfiles
{
    $f = $File::Find::name;
    if ($f =~ m/\.h$/ or $f =~ m/\.cpp$/)
    {
        $q = basename($f);

        # Skip if we're already in the script's own processing (avoid recursion on .bak)
        return if ($q =~ /\.bak$/);

        # Read the entire file
        open(IN, "<$q") || die "Can't open IN $q: $!";
        @lines = <IN>;
        close(IN);

        $content = join("", @lines);
        $modified = 0;

        # Generic replacement 1: namespace oldns1 { -> namespace newns1 {
        if ($old_ns1 ne $new_ns1 && $content =~ s/namespace\s+$old_ns1\s*\{/namespace $new_ns1 {/g) {
            $modified = 1;
            print "Fixed namespace 1 opening in $q\n";
        }

        # Generic replacement 2: namespace oldns2 { -> namespace newns2 {
        if ($old_ns2 ne $new_ns2 && $content =~ s/namespace\s+$old_ns2\s*\{/namespace $new_ns2 {/g) {
            $modified = 1;
            print "Fixed namespace 2 opening in $q\n";
        }

        # Generic replacement 3: } // namespace oldns1 -> } // namespace newns1
        if ($old_ns1 ne $new_ns1 && $content =~ s/\}\s*\/\/\s*namespace\s+$old_ns1/} \/\/ namespace $new_ns1/g) {
            $modified = 1;
            print "Fixed namespace 1 closing comment in $q\n";
        }

        # Generic replacement 4: } // namespace oldns2 -> } // namespace newns2
        if ($old_ns2 ne $new_ns2 && $content =~ s/\}\s*\/\/\s*namespace\s+$old_ns2/} \/\/ namespace $new_ns2/g) {
            $modified = 1;
            print "Fixed namespace 2 closing comment in $q\n";
        }

        # Generic replacement 5: oldns1::oldns2:: -> newns1::newns2::
        if ($content =~ s/\Q$old_ns1\E::\Q$old_ns2\E::/$new_ns1::$new_ns2::/g) {
            $modified = 1;
            print "Fixed namespace references in $q\n";
        }

        # Generic replacement 6: namespace alias = oldns1::... -> namespace alias = newns1::...
        if ($old_ns1 ne $new_ns1 && $content =~ s/(namespace\s+\w+\s*=\s*)\Q$old_ns1\E::/${1}${new_ns1}::/g) {
            $modified = 1;
            print "Fixed namespace alias in $q\n";
        }

        # Critical fix: Ensure closing braces for multi-level namespaces are on separate lines
        # Look for: } // namespace ns3 } // namespace ns2 } // namespace ns1
        # and replace with proper multi-line format
        if ($content =~ s/\}\s*\/\/\s*namespace\s+(\w+)\s*\}\s*\/\/\s*namespace\s+\Q$old_ns2\E\s*\}\s*\/\/\s*namespace\s+\Q$old_ns1\E/} \/\/ namespace $1\n} \/\/ namespace $new_ns2\n} \/\/ namespace $new_ns1/g) {
            $modified = 1;
            print "Fixed multi-level namespace closing braces in $q\n";
        }

        # Update plugin ID if it contains the old namespace
        # Pattern: org.oldns1.oldns2 or similar
        if ($content =~ s/org\.\Q$old_ns1\E\.\Q$old_ns2\E/org.$new_ns1.$new_ns2/g) {
            $modified = 1;
            print "Fixed plugin ID in $q\n";
        }

        # Only write if modified
        if ($modified) {
            open(OUT, "> ${q}.bak") || die "Can't open BAK ${q}.bak: $!";
            print OUT $content;
            close(OUT);
            system("mv ${q}.bak $q");
            $files_modified++;
        }
    }
}
