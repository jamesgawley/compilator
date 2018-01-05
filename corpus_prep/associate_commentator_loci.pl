# It is necessary to associate each one of the line-based Lucan and Virgil loci with a phrase-based locus.
# Each phrase-based locus is associated with a range of line loci.
# Each commentator parallel is associated with a range of line loci.
# Wherever there is overlap, the two loci should be associated.
# This will include some 'noise', as some phrases represent a small part of a line, and some commentator loci include much more than a single phrase.
# Expected CSV headers: 'TARGET_START', 'TARGET_STOP', 'SOURCE_START', 'SOURCE_STOP'
# Known issues: saving a CSV document from an Excel file creates problems with newlines; this script will read a Microsoft-created CSV file as a single line of text.
use strict;
use warnings;
binmode(STDOUT, ":utf8");
use utf8;
use Data::Dumper;

# open the necessary files
open (my $com, "<:utf8", $ARGV[0]) or die $! . "Specify a CSV file containing commentator parallels as the first argument when calling this script.";

open (my $res, "<:utf8", $ARGV[1]) or die $! . "Specify a results CSV file containing associated loci for the target and source as the second argument when calling this script.";

open (OUT, ">:utf8", $ARGV[2]) or die $! . "Specify a file where results can be saved as the third argument when calling this script.";

# create a map of array locations for each column. Resulting data structure is a hash with strings from the CSV header as keys and their array positions as values.

my $com_head = getHead($com);

my $res_head = getHead($res);

my $com_obj = makeRecords($com, $com_head);

my $res_obj = makeRecords($res, $res_head);

my @commentary;

foreach my $record (@{$com_obj}) {

	my %line_hash = %$record;

	# build an object like this: [target_book][target_line][source_book] = (source_line1, source_line2), with each line in a given range counted.
	
	for my $target_line ($line_hash{'TARGET_START'}..$line_hash{'TARGET_STOP'}) {
	
		for my $source_line ($line_hash{'SOURCE_START'}..$line_hash{'SOURCE_STOP'}) {
		
			push (@{$commentary[$line_hash{'TARGET_BOOK'}][$target_line][$line_hash{'SOURCE_BOOK'}]}, $source_line);
		
		}
		
	}

}

print OUT join (",", ('TARGET_START', 'TARGET_STOP', 'SOURCE_START', 'SOURCE_STOP'));

foreach my $record (@{$res_obj}) {

	my %line_hash = %$record;

	my $result = "FALSE";

	my %com_sources = ();
	
	my %vor_sources = ();

	#grab the book and line number
	for my $target_line ($line_hash{'TARGET_START'}..$line_hash{'TARGET_STOP'}) {
	
		for my $source_line ($line_hash{'SOURCE_START'}..$line_hash{'SOURCE_STOP'}) {
		
			#build the list of source lines for each index
		
			#the deref below access a list of source line like this [target_book][target_line][source_book] = (source_line1, source_line2), and adds them as hash keys.
			foreach my $com_line (@{$commentary[$line_hash{'TARGET_BOOK'}][$target_line][$line_hash{'SOURCE_BOOK'}]}) {
			
				$com_sources{$com_line} = 1;
			
			}
		
			$vor_sources{$source_line} = 1;
		}
		
	}
	
	foreach my $vortex_line (keys %vor_sources) {
	
		if ($com_sources{$vortex_line}) {
		
			$result = "TRUE";
		
		}
	
	}

	print OUT "\n" . join(",", @line_hash{'TARGET_BOOK', 'TARGET_START', 'TARGET_STOP', 'SOURCE_BOOK', 'SOURCE_START', 'SOURCE_STOP'}) . ",$result";

}




# take a list of start-stop loci and parse them to isolate book and line numbers.
sub getLines {

	# Reconstruct the hash inside the subroutine
	
	my %hash;
	
	my @return;
	
	@hash {'TARGET_START', 'TARGET_STOP', 'SOURCE_START', 'SOURCE_STOP'} = @_;
		
	@return[(0,1)] =  $hash{'TARGET_START'} =~ /(\d+)_(\d+)/; 
	
	(my $stop_book, $return[2]) = $hash{'TARGET_STOP'} =~ /(\d+)_(\d+)/;
	
	# if the start and stop book aren't the same, skip it.
	
	if ($return[0] != $stop_book) {
	
		for my $p (0..5) {
		
			$return[$p] = 0;
		
		}
		
		return @return;
	
	}
	
	@return[(3,4)] = $hash{'SOURCE_START'} =~ /(\d+)_(\d+)/;

	($stop_book, $return[5]) = $hash{'SOURCE_STOP'} =~ /(\d+)_(\d+)/;
	
	if ($return[3] != $stop_book) {
	
		for my $p (0..5) {
		
			$return[$p] = 0;
		
		}
		
	
			
		return @return;
	
	}

	return @return;

}

sub getHead {

	my $file = shift;

	my $first = <$file>;

	chomp($first);
	
	$first =~ s/\s//g;

	my @header = split(',', $first);

	my %head;

	@head{ @header } = (0..$#header);

	return \%head;

}


sub makeRecords {

	my ($file_ref, $head_ref) = @_;

	my @index;

	while (<$file_ref>) {

		chomp;

		my @line_array = split(",", $_);

		my %line_hash;

		@line_hash {'TARGET_BOOK', 'TARGET_START', 'TARGET_STOP', 'SOURCE_BOOK', 'SOURCE_START', 'SOURCE_STOP'} = getLines(@line_array[@$head_ref {'TARGET_START', 'TARGET_STOP', 'SOURCE_START', 'SOURCE_STOP'}]);

#		print "\n" . join ("\t", ('TARGET_START', 'TARGET_STOP', 'SOURCE_START', 'SOURCE_STOP'));
	
#		print "\n" . join("\t", @line_array[@$head_ref {'TARGET_START', 'TARGET_STOP', 'SOURCE_START', 'SOURCE_STOP'}]) . "\n";
	
#		print "\n" . join ("\t", ('TARGET_BOOK', 'TARGET_START', 'TARGET_STOP', 'SOURCE_BOOK', 'SOURCE_START', 'SOURCE_STOP'));
	
#		print "\n" . join("\t", @line_hash{'TARGET_BOOK', 'TARGET_START', 'TARGET_STOP', 'SOURCE_BOOK', 'SOURCE_START', 'SOURCE_STOP'}) . "\n";
	
#		my $useless = <STDIN>;	


		push (@index, \%line_hash);

	}

	
	return \@index;

}











