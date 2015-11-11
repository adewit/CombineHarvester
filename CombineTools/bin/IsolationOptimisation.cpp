#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"

using namespace std;

int main() {
  //! [part1]
  // First define the location of the "auxiliaries" directory where we can
  // source the input files containing the datacard shapes
  
  typedef vector<string> VString;
  typedef vector<pair<int, string>> Categories;
  string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/shapes/";
  string input_dir =
      string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/CombineTools/input";

  VString chns =
      {"et"};

  map<string, string> input_folders = {
      {"et", "Imperial"},
      {"em", "Imperial"},
  };

  map<string, VString> bkg_procs;
  bkg_procs["et"] = {"W", "QCD", "ZL", "ZJ", "TT", "VV"};
  bkg_procs["em"] = {"QCD", "ZLL", "TT", "VV"};


  // Create an empty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.
  ch::CombineHarvester cb;
  // Uncomment this next line to see a *lot* of debug information
  // cb.SetVerbosity(3);

  // Here we will just define two categories for an 8TeV analysis. Each entry in
  // the vector below specifies a bin name and corresponding bin_id.
  //
  map<string,Categories> cats;
  cats["et_13TeV"] = {
/*      {1, "eleTau_db03iso0p07"}, {2, "eleTau_db03iso0p08"},
      {3, "eleTau_db03iso0p09"}, {4, "eleTau_db03iso0p1"},
      {5, "eleTau_db03iso0p11"}, {6, "eleTau_db03iso0p12"}, 
      {7, "eleTau_db03iso0p13"},
      {11, "eleTau_db03allchiso0p07"}, {12, "eleTau_db03allchiso0p08"},
      {13, "eleTau_db03allchiso0p09"}, {14, "eleTau_db03allchiso0p1"},
      {15, "eleTau_db03allchiso0p11"}, {16, "eleTau_db03allchiso0p12"}, 
      {17, "eleTau_db03allchiso0p13"},
      {21, "eleTau_db04allchiso0p07"}, {22, "eleTau_db04allchiso0p08"},
      {23, "eleTau_db04allchiso0p09"}, {24, "eleTau_db04allchiso0p1"},
      {25, "eleTau_db04allchiso0p11"}, {26, "eleTau_db04allchiso0p12"}, 
      {27, "eleTau_db04allchiso0p13"},
      {31, "eleTau_ea03iso0p07"}, {32, "eleTau_ea03iso0p08"},
      {33, "eleTau_ea03iso0p09"}, {34, "eleTau_ea03iso0p1"},
      {35, "eleTau_ea03iso0p11"}, {36, "eleTau_ea03iso0p12"}, 
      {37, "eleTau_ea03iso0p13"}}*/
      {41, "eleTau_ea03iso0p14"},{42, "eleTau_ea03iso0p15"},
      {43, "eleTau_ea03iso0p16"},{44, "eleTau_ea03iso0p17"},
      {45, "eleTau_ea03iso0p18"}, {51, "eleTau_db04allchiso0p14"},
      {52, "eleTau_db04allchiso0p15"},{53,"eleTau_db04allchiso0p16"},
      {54, "eleTau_db04allchiso0p17"},{55,"eleTau_db04allchiso0p18"}};


  cats["em_13TeV"] = {
      {1, "emu_isoe0p13"}, {2, "emu_isoe0p14"},
      {3, "emu_isoe0p15"}, {4, "emu_isoe0p16"},
      {5, "emu_isoe0p17"}};


/*  ch::Categories cats = {
      {1, "emu_isoe0p13"},
      {2, "emu_isoe0p14"},
      {3, "emu_isoe0p15"},
      {4, "emu_isoe0p16"},
      {5, "emu_isoe0p17"},
      {6, "emu_isoe0p01"},
    };
*/
  // ch::Categories is just a typedef of vector<pair<int, string>>
  //! [part1]


  //! [part2]
//  vector<string> masses = ch::MassesFromRange("120-135:5");
  // Or equivalently, specify the mass points explicitly:
      //vector<string> masses = {"90"};
  //! [part2]

  //! [part3]
    vector<string> sig_procs = {"ZTT"};
  for(auto chn : chns){
    cb.AddObservations({"*"}, {"htt"}, {"13TeV"}, {chn}, cats[chn+"_13TeV"]);
  //! [part3]

  //! [part4]
//  vector<string> bkg_procs = {"ZTT", "ZLL", "QCD", "TT", "VV"};
    cb.AddProcesses({"*"}, {"htt"}, {"13TeV"}, {chn}, bkg_procs[chn], cats[chn+"_13TeV"], false);

  
    cb.AddProcesses({"*"}, {"htt"}, {"13TeV"}, {chn}, sig_procs, cats[chn+"_13TeV"], true);
    }
  //! [part4]


  //Some of the code for this is in a nested namespace, so
  // we'll make some using declarations first to simplify things a bit.
  using ch::syst::SystMap;
  using ch::syst::era;
  using ch::syst::bin_id;
  using ch::syst::process;


  //! [part5]
  cb.cp().signals()
      .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<era>::init
      ({"7TeV"}, 1.022)
      ({"8TeV"}, 1.026)
      ({"13TeV"}, 1.026));
  //! [part5]

  //! [part6]
  cb.cp().process({"ggH"})
      .AddSyst(cb, "pdf_gg", "lnN", SystMap<>::init(1.097));

//  cb.cp().process(ch::JoinStr({sig_procs, {"ZTT", "TT"}}))
 //     .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

  cb.cp().process(ch::JoinStr({sig_procs, {"TT","VV","ZLL"}})).channel({"em"})
      .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.02));

  cb.cp().channel({"em"}).AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

  cb.cp().channel({"em"}).AddSyst(cb, "CMS_scale_j_13TeV", "lnN", SystMap<era,process>::init
      ({"13TeV"}, {"TT"},          0.91)
      ({"13TeV"}, {"VV"},            0.98));


  cb.cp().process(ch::JoinStr({sig_procs, {"TT","VV","ZL","W","ZJ"}})).channel({"et"})
      .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.02));
  
  cb.cp().process({"TT","VV","ZL","W","ZJ"}).AddSyst(cb, "lumi_13TeV", "lnN", SystMap<>::init(1.026));

  cb.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));

  cb.cp().channel({"em"}).process({"ZLL"}).AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));
  cb.cp().channel({"et"}).process({"ZL","ZJ"}).AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));

  cb.cp().process({"TT"})
      .AddSyst(cb, "CMS_htt_ttbarNorm_13TeV", "lnN", SystMap<era>::init
        ({"13TeV"}, 1.10));

  cb.cp().process({"QCD"}).channel({"em"}).AddSyst(cb,
      "CMS_htt_em_QCD_13TeV","lnN",SystMap<>::init(1.3));

 cb.cp().process({"QCD"}).channel({"et"}).AddSyst(cb,
      "CMS_htt_et_QCD_13TeV","lnN",SystMap<>::init(1.3));


  cb.cp().process({"VV"}).AddSyst(cb,
      "CMS_htt_VVNorm_13TeV", "lnN", SystMap<>::init(1.15));

  cb.cp().process({"W"}).channel({"et"}).AddSyst(cb,
     "CMS_htt_WNorm_13TeV","lnN",SystMap<>::init(1.2));





/*  cb.cp()
      .AddSyst(cb,
        "CMS_scale_j_$ERA", "lnN", SystMap<era, bin_id, process>::init
        ({"8TeV"}, {1},     {"ggH"},        1.04)
        ({"8TeV"}, {1},     {"qqH"},        0.99)
        ({"8TeV"}, {2},     {"ggH"},        1.10)
        ({"8TeV"}, {2},     {"qqH"},        1.04)
        ({"8TeV"}, {2},     {"TT"},         1.05));
*/

//  cb.cp().process(ch::JoinStr({sig_procs, {"ZTT"}}))
 //     .AddSyst(cb, "CMS_scale_t_mutau_$ERA", "shape", SystMap<>::init(1.00));
  //! [part6]

  //! [part7]
  for (string chn:chns){
    cb.cp().channel({chn}).backgrounds().ExtractShapes(
        aux_shapes + "Imperial/htt_"+chn+".inputs-sm-13TeV-mvis-Oct26EXT.root",
        "$BIN/$PROCESS",
        "$BIN/$PROCESS_$SYSTEMATIC");
    cb.cp().channel({chn}).signals().ExtractShapes(
        aux_shapes + "Imperial/htt_"+chn+".inputs-sm-13TeV-mvis-Oct26EXT.root",
        "$BIN/$PROCESS",
        "$BIN/$PROCESS_$SYSTEMATIC");
   }

/*  cout << ">> Undoing scaling of signal process rates...\n";
  for (string const& p: sig_procs) {
    cb.cp().process({p}).era({"13TeV"}).ForEachProc([&](ch::Process *proc){
      proc->set_rate(proc->rate()*(double)(1./6025));
    });
  }*/

  //map<string, TGraph> xs;
  // Get the table of H->tau tau BRs vs mass
  //xs["htt"] = ch::TGraphFromTable(input_dir+"/xsecs_brs/htt_YR3.txt", "mH", "br");
  /*for (string const& e : {"13TeV"}) {
    for (string const& p : sig_procs) {
      // Get the table of xsecs vs mass for process "p" and era "e":
      xs[p+"_"+e] = ch::TGraphFromTable(input_dir+"/xsecs_brs/"+p+"_"+e+"_YR3.txt", "mH", "xsec");
      cout << ">>>> Scaling for process " << p << " and era " << e << "\n";
      cb.cp().process({p}).era({e}).ForEachProc([&](ch::Process *proc) {
        double m = boost::lexical_cast<double>(proc->mass());
        proc->set_rate(proc->rate() * xs[p+"_"+e].Eval(m) * xs["htt"].Eval(m));
      });
    }
  }*/
  

  //! [part7]
  ////

  //! [part8]
  /*auto bbb = ch::BinByBinFactory()
    .SetAddThreshold(0.1)
    .SetFixNorm(true);

  bbb.AddBinByBin(cb.cp().backgrounds(), cb);
*/

  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  // which is commonly used in the htt analyses
  ch::SetStandardBinNames(cb);
  //! [part8]

  //! [part9]
  // First we generate a set of bin names:
  set<string> bins = cb.bin_set();
  // This method will produce a set of unique bin names by considering all
  // Observation, Process and Systematic entries in the CombineHarvester
  // instance.

  // We create the output root file that will contain all the shapes.

  // Finally we iterate through each bin,mass combination and write a
  // datacard.
  for (string chn : chns) {
    TFile output(("htt_" + chn + ".input.root").c_str(),
                 "RECREATE");
    auto bins = cb.cp().channel({chn}).bin_set();
    for (auto b : bins) {
//      for (auto m : masses) {
        cout << ">> Writing datacard for bin: " << b //<< " and mass: " << m
                  << "\r" << flush;
        cb.cp().channel({chn}).bin({b}).WriteDatacard(
            b+"_"+".txt", output);
    }
    output.Close();
  }

  //! [part9]

}
