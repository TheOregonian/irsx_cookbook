output_streams = {
    'employees': {  
        'filename':'employees_detailed', # will output to employees_detailedYYYY.csv where year is specified below
        'headers':["object_id", "name", "business_name1", "title", "org_comp", "related_comp", "other_cmp", "form", "source","ein"]
    },
    'salaries': {  
        'filename':'filer_comp', # will output to filer_compYYYY.csv where year is specified below
        'headers':["year", "ein", "object_id", "form", "source", "compensation", "income", "revenue", "assets", "expenses"]
    },
    'states': {
        'filename':'filer_states',
        'headers':["ein","state"]
    },
    'exempt': {
        'filename':'filer_exempt',
        'headers':["ein","org527",'org501c','org4947','org501c3']
    },
    'expenses': {
        'filename':'filer_expenses',
        'headers':["ein","object_id","prog_exp"]
    },
    'assets': {
        'filename':'filer_assets',
        'headers':["ein","object_id","assets_pf"]
    }


}





# The format we're using is this
# The stream_key used must be defined in the output stream above.

data_capture_dict = {
    'ReturnHeader990x': {
        'parts': {
            'returnheader990x_part_i': {
                'stream_key': 'states',  # 'stream_key' specifies where the output goes--must exist as a key in output_streams
                'ein': {'header':'ein'},
                'USAddrss_SttAbbrvtnCd':{'header':'state'},
            }

        },
    },
    'IRS990': {
        'parts': {
            'part_0': {
                'stream_key': 'exempt',
                'ein': {'header': 'ein'},
                'Orgnztn527Ind': {'header': 'org527'},
                'Orgnztn501cInd': {'header': 'org501c'},
                'Orgnztn49471NtPFInd': {'header': 'org4947'},
                'Orgnztn501c3Ind': {'header': 'org501c3'},

            },
            'part_i': {
                'stream_key': 'salaries',  # 'stream_key' specifies where the output goes--must exist as a key in output_streams
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'CYSlrsCmpEmpBnftPdAmt':{'header':'compensation','default':0},
                'CYRvnsLssExpnssAmt':{'header':'income','default':0},
                'CYTtlRvnAmt':{'header':'revenue','default':0},
                'TtlAsstsEOYAmt':{'header':'assets','default':0},
                'CYTtlExpnssAmt':{'header':'expenses','default':0},
            },
            'part_ix': {
                'stream_key': 'expenses',  # 'stream_key' specifies where the output goes--must exist as a key in output_streams
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'TtlFnctnlExpnss_TtlAmt': {'header':'func_exp','default':0},
                'TtlFnctnlExpnss_PrgrmSrvcsAmt': {'header':'prog_exp','default':0}
                
            }

        },
        ## The remaining logic is for capturing salaries wherever they appear in 
        ## the 990, 990PF and 990EZ
        'groups': {
             'Frm990PrtVIISctnA': {
                'stream_key': 'employees',  # 'stream_key' specifies where the output goes--must exist as a key in output_streams
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'PrsnNm': {'header':'name'},
                'BsnssNmLn1Txt':{'header':'business_name1'},
                'TtlTxt': {'header':'title'},
                'RprtblCmpFrmOrgAmt': {
                    'header':'org_comp',
                    'default':0  # set numeric if missing
                },
                'RprtblCmpFrmRltdOrgAmt': {
                    'header':'related_comp',
                    'default':0
                },
                'OthrCmpnstnAmt':{
                    'header':'other_cmp',
                    'default':0
                }
            }
        }
    },
    'IRS990EZ': {
        'parts': {
            'ez_part_i': {
                'stream_key': 'salaries',  # 'stream_key' specifies where the output goes--must exist as a key in output_streams
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'SlrsOthrCmpEmplBnftAmt':{'header':'compensation','default':0},
                'ExcssOrDfctFrYrAmt':{'header':'income','default':0},
                'TtlRvnAmt':{'header':'revenue','default':0},
                'NtAsstsOrFndBlncsEOYAmt':{'header':'assets','default':0},
                'TtlExpnssAmt':{'header':'expenses','default':0}
            }
        },
        'groups': {
            'EZOffcrDrctrTrstEmpl': {
                'stream_key': 'employees',
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'PrsnNm': {'header':'name'},
                'BsnssNmLn1': {'header':'business_name1'},


                'TtlTxt': {'header':'title'},
                'CmpnstnAmt': {
                    'header':'org_comp',
                    'default':0
                },
                'related_comp': {'header':'related_comp','default':0},
                'composite': {  # other compensation includes benefits and other allowances for EZ, PF filers
                    'other_cmp': {
                        'EmplyBnftPrgrmAmt': {
                            'default':0
                        },
                        'ExpnsAccntOthrAllwncAmt': {
                            'default':0
                        }
                    }
                }
            },
            'EZCmpnstnHghstPdEmpl': {
                'stream_key': 'employees',
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'PrsnNm': {'header':'name'},
                'TtlTxt': {'header':'title'},
                'CmpnstnAmt': {
                    'header':'org_comp',
                    'default':0
                },
                'related_comp': {'header':'related_comp','default':0},
                'composite': {
                    'other_cmp': {
                        'EmplyBnftsAmt': {
                            'default':0
                        },
                        'ExpnsAccntAmt': {
                            'default':0
                        }
                    }
                }
            }
        }
    },
    'IRS990PF': {
        'parts': {
            'pf_part_i': {
                'stream_key': 'salaries',  # 'stream_key' specifies where the output goes--must exist as a key in output_streams
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'CmpOfcrDrTrstRvAndExpnssAmt':{'header':'compensation','default':0},
                'income': {'header':'income','default':0},
                'TtlRvAndExpnssAmt':{'header':'revenue','default':0},
                'TtlExpnssRvAndExpnssAmt':{'header':'expenses','default':0}
            },
            'pf_part_ii': {
                'stream_key': 'assets',  # 'stream_key' specifies where the output goes--must exist as a key in output_streams
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'TtlAsstsEOYFMVAmt':{'header':'assets_pf','default':0},
            }
        },
        'groups': {
            'PFOffcrDrTrstKyEmpl': {
                'stream_key': 'employees',

                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'OffcrDrTrstKyEmpl_PrsnNm': {'header':'name'},
                'OffcrDrTrstKyEmpl_BsnssNmLn1': {'header':'business_name1'},
                'OffcrDrTrstKyEmpl_TtlTxt': {'header':'title'},
                'OffcrDrTrstKyEmpl_CmpnstnAmt': {
                    'header':'org_comp',
                    'default':0  # set numeric if missing
                },
                'composite': {
                    'other_cmp': {
                        'OffcrDrTrstKyEmpl_EmplyBnftPrgrmAmt': {
                            'default':0
                        },
                        'OffcrDrTrstKyEmpl_ExpnsAccntOthrAllwncAmt': {
                            'default':0
                        }
                    }
                }
            },
            'PFCmpnstnHghstPdEmpl': {
                'stream_key': 'employees',

                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'CmpnstnHghstPdEmpl_PrsnNm': {'header':'name'},
                'CmpnstnHghstPdEmpl_TtlTxt': {'header':'title'},
                'CmpnstnHghstPdEmpl_CmpnstnAmt': {
                    'header':'org_comp',
                    'default':0  # set numeric if missing
                },
                'composite': {
                    'other_cmp': {
                        'CmpnstnHghstPdEmpl_EmplyBnftsAmt': {
                            'default':0
                        },
                        'CmpnstnHghstPdEmpl_ExpnsAccntAmt': {
                            'default':0
                        }
                    }
                }
            }
        }
    }
}




from stream_extractor import StreamExtractor
import unicodecsv as csv




YEAR = 2018  # THIS MUST AGREE WITH OUR OTHER DATA
extractor = StreamExtractor(output_streams, data_capture_dict, YEAR)




# read the whole file of orgs with efilings from part 1 here, it's not very long
file_rows = [] 
# We're using the output of part 1
with open('orefilers.csv', 'rb') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        file_rows.append(row)
        
        
        
        
for filing_count, row in enumerate(file_rows):
    this_object_id = row['OBJECT_ID']
    tax_period = row['TAX_PERIOD_y']
    # don't need to pass taxpayer name in, but makes the output more readable
#     extractor.run_filing(this_object_id, taxpayer_name=row['TAXPAYER_NAME'])
    extractor.run_filing(this_object_id)
    filing_count += 1
    if filing_count % 100 == 0:
        print("Processed %s filings" % filing_count)
    
print("end")




import pandas as pd
data = pd.read_csv("filer_comp2018.csv")
data.head()




# drop older object_ids from filer_comp
dfsorted = data.sort_values('object_id', ascending=False).drop_duplicates(subset=['ein'])
dfsorted = dfsorted.drop(['year','form','source'],axis=1)
dfsorted.head()




#join orefilers data to org compensation file
tax = pd.read_csv("orefilers.csv",usecols=[6,7,9,12,13,14,15,19,20])
ntee = pd.read_csv("ntee.csv",usecols=[0,1])
joined = dfsorted.join(tax.set_index('OBJECT_ID'), on='object_id')
joined['ntee'] = joined['NTEE_CD'].str[:3]
#join NTEE category and drop ntee code
joined = joined.join(ntee.set_index('NTEE'), on='ntee')
joined = joined.drop(['NTEE_CD','ntee'],axis=1)
joined = joined.rename(columns={"TAX_PERIOD_y": "tax_period", "Code": "ntee"})
joined.set_index('ein', inplace=True)
values = {'compensation': 0,'income': 0,'assets': 0,'revenue': 0,'expenses':0,'tax_period': 0}
joined.fillna(value=values,inplace=True)
joined = joined.astype({'compensation': 'int64','income': 'int64','revenue': 'int64','assets': 'int64','expenses': 'int64','tax_period': 'int64'})
joined.head()
#join program expenses
exp = pd.read_csv("filer_expenses2018.csv",usecols=[1,2])
withexp = joined.join(exp.set_index('object_id'), on='object_id')
#join foundation assets
assets = pd.read_csv("filer_assets2018.csv",usecols=[1,2])
withassets = withexp.join(assets.set_index('object_id'), on='object_id')
ass_zero = {'assets_pf': 0,'prog_exp':0}
withassets.fillna(value=ass_zero,inplace=True)
withassets['assets'] = withassets['assets']+withassets['assets_pf']
withassets = withassets.astype({'assets': 'int64','prog_exp':'int64'})
withassets.drop(['assets_pf'],axis=1,inplace=True)
withassets.head()




#get ids of non-oregon filers
states = pd.read_csv("filer_states2018.csv")
states.set_index('ein', inplace=True)
indexNames = states[ states['state'] != "OR" ].index
# Delete non-oregon filers
justore = withassets.drop(indexNames)
justore = justore[['object_id','TAXPAYER_NAME','STREET','CITY','STATE','ZIP','compensation','income','revenue','assets','expenses','prog_exp','tax_period','RETURN_TYPE','ntee']]
justore.head()
justore.to_csv("np_org_comp_2018.csv")





#read employees and drop dupes
data = pd.read_csv("employees_detailed2018.csv")
data = data.drop_duplicates()
data['org_id'] = data['ein']
ore_emp = data.set_index('ein').drop(indexNames)
ore_emp.reset_index(drop=True,inplace=True)
ore_emp.head()




#strip out employees who received no income from local org
local_emp = ore_emp[ore_emp.org_comp>0]
#make NaN's blank and concatenate name and business_name1 fields
values = {'related_comp': 0}
local_emp = local_emp.fillna(value=values)
local_emp = local_emp.astype({'related_comp': 'int64'})
local_emp = local_emp.fillna('')
local_emp.insert(3, 'emp_name', local_emp['name']+local_emp['business_name1'])
local_emp = local_emp.drop(['name','business_name1'],axis=1)
local_emp['emp_name'] = local_emp['emp_name'].str.upper()
local_emp['title'] = local_emp['title'].str.upper()

#sum compensation fields
local_emp.insert(6,'total_comp',local_emp.iloc[:, 3:6].sum(axis=1))
local_emp.reset_index(drop=True,inplace=True)
local_emp.rename_axis("id",inplace=True)
local_emp.to_csv("np_emp_comp_2018.csv")
local_emp.head()





