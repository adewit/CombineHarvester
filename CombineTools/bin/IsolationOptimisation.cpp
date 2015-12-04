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
      {"em","mt"};

  map<string, string> input_folders = {
      {"et", "Imperial"},
      {"em", "Imperial"},
      {"mt", "Imperial"},
      {"tt", "Imperial"},
  };

  map<string, VString> bkg_procs;
  bkg_procs["et"] = {"W", "QCD", "ZL", "ZJ", "TT", "VV"};
  bkg_procs["em"] = {"QCD", "ZLL", "TT", "VV"};
  bkg_procs["mt"] = {"QCD","W","ZL","ZJ","TT","VV"};
  bkg_procs["tt"] = {"QCD", "ZL","ZJ","W","VV","TT"};


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
    {1,"et_ea03iso0p07"},{2, "et_ea03iso0p08"},
    {3,"et_ea03iso0p09"},{4, "et_ea03iso0p1"},
    {5,"et_ea03iso0p11"},{6, "et_ea03iso0p12"},
    {7, "et_ea03iso0p13"},{8,"et_ea03iso0p14"},
    {9, "et_ea03iso0p15"} ,{10, "et_ea03iso0p16"},
    {11, "et_ea03iso0p17"},{12, "et_ea03iso0p18"},
/*    {21,"et_db04allchiso0p07"},{22, "et_db04allchiso0p08"},
    {23,"et_db04allchiso0p09"},{24, "et_db04allchiso0p1"},
    {25,"et_db04allchiso0p11"},{26, "et_db04allchiso0p12"},
    {27, "et_db04allchiso0p13"},{28,"et_db04allchiso0p14"},
    {29, "et_db04allchiso0p15"} ,{30, "et_db04allchiso0p16"},
    {31, "et_db04allchiso0p17"},{32, "et_db04allchiso0p18"}
*/
/*{1,"et_incvlelm"},{2,"et_incvletm"},
{3,"et_inclelm"},{4,"et_incletm"},
{5,"et_incmelm"},{6,"et_incmetm"},
{7,"et_inctelm"},{8,"et_inctetm"},
{9,"et_incvtelm"},{10,"et_incvtetm"},
{11,"et_dbloose"},{12,"et_dbmedium"},
{13,"et_dbtight"},{14,"et_pwloose"},
{15,"et_pwmedium"},{16,"et_pwtight"},
{17,"et_mvavloose"},{18,"et_mvaloose"},
{19,"et_mvamedium"},{20,"et_mvatight"},
{21,"et_mvavtight"}*/
};
   
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
/*      {41, "eleTau_ea03iso0p14"},{42, "eleTau_ea03iso0p15"},
      {43, "eleTau_ea03iso0p16"},{44, "eleTau_ea03iso0p17"},
      {45, "eleTau_ea03iso0p18"}, {51, "eleTau_db04allchiso0p14"},
      {52, "eleTau_db04allchiso0p15"},{53,"eleTau_db04allchiso0p16"},
      {54, "eleTau_db04allchiso0p17"},{55,"eleTau_db04allchiso0p18"}*/


 cats["mt_13TeV"] = {
/*{1,"mt_incvlelm"},{2,"mt_incvletm"},
{3,"mt_inclelm"},{4,"mt_incletm"},
{5,"mt_incmelm"},{6,"mt_incmetm"},
{7,"mt_inctelm"},{8,"mt_inctetm"},
{9,"mt_incvtelm"},{10,"mt_incvtetm"},
{11,"mt_dbloose"},{12,"mt_dbmedium"},
{13,"mt_dbtight"},{14,"mt_pwloose"},
{15,"mt_pwmedium"},{16,"mt_pwtight"},
{17,"mt_mvavloose"},{18,"mt_mvaloose"},
{19,"mt_mvamedium"},{20,"mt_mvatight"},
{21,"mt_mvavtight"}*/

    /*{1,"mt_trk03iso0p07"},{2, "mt_trk03iso0p08"},
    {3,"mt_trk03iso0p09"},{4, "mt_trk03iso0p1"},
    {5,"mt_trk03iso0p11"},{6, "mt_trk03iso0p12"},
    {7, "mt_trk03iso0p13"},{8,"mt_trk03iso0p14"},
    {9, "mt_trk03iso0p15"} ,{10, "mt_trk03iso0p16"},
    {11, "mt_trk03iso0p17"},{12, "mt_trk03iso0p18"},*/
/*   {1,"mt_puw03iso0p05"},{2,"mt_puw03iso0p1"},
   {3,"mt_puw03iso0p15"},{4,"mt_puw04iso0p05"},
   {5,"mt_puw04iso0p1"},{6,"mt_puw04iso0p15"}
*/
  {1,"mt_trk03iso0p02"},{2,"mt_trk03iso0p03"},
  {3,"mt_trk03iso0p04"},{4,"mt_trk03iso0p05"},
  {6,"mt_trk03iso0p06"}
/*
    {21,"mt_db03allchiso0p07"},{22, "mt_db03allchiso0p08"},
    {23,"mt_db03allchiso0p09"},{24, "mt_db03allchiso0p1"},
    {25,"mt_db03allchiso0p11"},{26, "mt_db03allchiso0p12"},
    {27, "mt_db03allchiso0p13"},{28,"mt_db03allchiso0p14"},
    {29, "mt_db03allchiso0p15"} ,{30, "mt_db03allchiso0p16"},
    {31, "mt_db03allchiso0p17"},{32, "mt_db03allchiso0p18"},
    {41,"mt_db04allchiso0p07"},{42, "mt_db04allchiso0p08"},
    {43,"mt_db04allchiso0p09"},{44, "mt_db04allchiso0p1"},
    {45,"mt_db04allchiso0p11"},{46, "mt_db04allchiso0p12"},
    {47, "mt_db04allchiso0p13"},{48,"mt_db04allchiso0p14"},
    {49, "mt_db04allchiso0p15"} ,{50, "mt_db04allchiso0p16"},
    {51, "mt_db04allchiso0p17"},{52, "mt_db04allchiso0p18"},
    {61,"mt_db04iso0p11"},{62, "mt_db04iso0p12"},
    {63, "mt_db04iso0p13"},{64,"mt_db04iso0p14"},
    {65, "mt_db04iso0p15"} ,{66, "mt_db04iso0p16"},
    {67, "mt_db04iso0p17"},{68, "mt_db04iso0p18"}};
*/
};


  cats["em_13TeV"] = {
   /*{1,"em_mpuw03iso0p05"},{2,"em_mpuw03iso0p1"},
   {3,"em_mpuw03iso0p15"},{4,"em_mpuw04iso0p05"},
   {5,"em_mpuw04iso0p1"},{6,"em_mpuw04iso0p15"}*/
   {1,"em_mtrk03iso0p05"},{2,"em_mtrk03iso0p06"},
   {3,"em_mtrk03iso0p07"},{4,"em_mtrk03iso0p08"}//,
//   {5,"em_mtrk03iso0p09"}

/*      {1, "em_mtrk03iso0p1"},{2,"em_mtrk03iso0p11"},
      {3, "em_mtrk03iso0p12"},{4,"em_mtrk03iso0p13"},
      {5, "em_mtrk03iso0p14"},{6,"em_mtrk03iso0p15"},
      {7, "em_mtrk03iso0p16"},{8,"em_mtrk03iso0p17"},
      {9, "em_mtrk03iso0p18"},{10,"em_mtrk03iso0p19"},
      {11,"em_mtrk03iso0p20"},{12,"em_mtrk03iso0p21"},*/
    /*  {21, "em_mdb04allchiso0p1"},{22,"em_mdb04allchiso0p11"},
      {23, "em_mdb04allchiso0p12"},{24,"em_mdb04allchiso0p13"},
      {25, "em_mdb04allchiso0p14"},{26,"em_mdb04allchiso0p15"},
      {27, "em_mdb04allchiso0p16"},{28,"em_mdb04iso0p17"},
      {29, "em_mdb04allchiso0p18"},{30,"em_mdb04allchiso0p19"},
      {31,"em_mdb04allchiso0p20"},{32,"em_mdb04allchiso0p21"},
*/
      /*{41, "em_eea03iso0p1"},{42,"em_eea03iso0p11"},
      {43, "em_eea03iso0p12"},{44,"em_eea03iso0p13"},
      {45, "em_eea03iso0p14"},{46,"em_eea03iso0p15"},
      {47, "em_eea03iso0p16"},{48,"em_eea03iso0p17"},
      {49, "em_eea03iso0p18"},{50,"em_eea03iso0p19"},
      {51,"em_eea03iso0p20"},{52,"em_eea03iso0p21"},*/
 /*     {61, "em_eea03allchiso0p1"},{62,"em_eea03allchiso0p11"},
      {63, "em_edb04allchiso0p12"},{64,"em_edb04allchiso0p13"},
      {65, "em_edb04allchiso0p14"},{66,"em_edb04allchiso0p15"},
      {67, "em_edb04allchiso0p16"},{68,"em_edb04iso0p17"},
      {69, "em_edb04allchiso0p18"},{70,"em_edb04allchiso0p19"},
      {71,"em_edb04allchiso0p20"},{72,"em_edb04allchiso0p21"}
*/
     };

  cats["tt_13TeV"] = {
/*{1,"tt_incvlelm"},{2,"tt_incvletm"},
{3,"tt_inclelm"},{4,"tt_incletm"},
{5,"tt_incmelm"},{6,"tt_incmetm"},
{7,"tt_inctelm"},{8,"tt_inctetm"},
{9,"tt_incvtelm"},{10,"tt_incvtetm"},
{11,"tt_dbloose"},{12,"tt_dbmedium"},
{13,"tt_dbtight"},{14,"tt_pwloose"},*/
{15,"tt_pwmedium"}/*,{16,"tt_pwtight"},
{17,"tt_mvavloose"},{18,"tt_mvaloose"},
{19,"tt_mvamedium"},{20,"tt_mvatight"},
{21,"tt_mvavtight"}*/

/*     {1, "tt_incvlelm"}, {2,"tt_incvletm"},
     {3, "tt_inclelm"}, {4, "tt_incletm"},
     {5, "tt_incmelm"}, {6, "tt_incmetm"},
     {7, "tt_inctelm"}, {8, "tt_inctetm"},
     {9, "tt_incvtelm"},{10,"tt_incvtetm"}*/};


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

  cb.cp().process(ch::JoinStr({sig_procs, {"TT","VV","ZLL","W"}})).channel({"em"})
      .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.02));

  cb.cp().process(ch::JoinStr({sig_procs, {"TT","VV","ZL","ZJ","W"}})).channel({"et"})
      .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.02));

  cb.cp().channel({"em"}).process(ch::JoinStr({sig_procs, {"TT","VV","ZLL","W"}})).AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));
  cb.cp().channel({"mt"}).process(ch::JoinStr({sig_procs, {"TT","VV","ZL","ZJ","W"}})).AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));


/*  cb.cp().channel({"em","et","mt","tt"}).AddSyst(cb, "CMS_scale_j_13TeV", "lnN", SystMap<era,process>::init
      ({"13TeV"}, {"TT"},          0.91)
      ({"13TeV"}, {"VV"},            0.98));*/


/*  cb.cp().process(ch::JoinStr({sig_procs, {"TT","VV","ZL","W","ZJ"}})).channel({"et"})
      .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.02));*/
  
  cb.cp().process({"TT","VV","ZL","W","ZJ"}).channel({"em"}).AddSyst(cb, "lumi_13TeV", "lnN", SystMap<>::init(1.026));

  cb.cp().process({"TT","VV","ZL","W","ZJ"}).channel({"et","mt","tt"}).AddSyst(cb, "lumi_13TeV", "lnN", SystMap<>::init(1.026));

  cb.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));

  cb.cp().channel({"em"}).process({"ZLL"}).AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));
  cb.cp().channel({"et","mt","em"}).process({"ZL","ZJ"}).AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));

  cb.cp().process({"TT"})
      .AddSyst(cb, "CMS_htt_ttbarNorm_13TeV", "lnN", SystMap<era>::init
        ({"13TeV"}, 1.10));

  cb.cp().process({"QCD"}).channel({"em"}).AddSyst(cb,
      "CMS_htt_em_QCD_13TeV","lnN",SystMap<>::init(1.3));

 cb.cp().process({"QCD"}).channel({"et","mt","tt"}).AddSyst(cb,
      "CMS_htt_et_QCD_13TeV","lnN",SystMap<>::init(1.3));


  cb.cp().process({"VV"}).AddSyst(cb,
      "CMS_htt_VVNorm_13TeV", "lnN", SystMap<>::init(1.15));

  cb.cp().process({"W"}).AddSyst(cb,
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
        aux_shapes + "Imperial/htt_"+chn+".inputs-sm-13TeV-mvis-AddPUW.root",
        "$BIN/$PROCESS",
        "$BIN/$PROCESS_$SYSTEMATIC");
    cb.cp().channel({chn}).signals().ExtractShapes(
        aux_shapes + "Imperial/htt_"+chn+".inputs-sm-13TeV-mvis-AddPUW.root",
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
