import argparse
import pandas as pd
from pathlib import Path
from utils import Config
from sklearn.model_selection import train_test_split


parser = argparse.ArgumentParser()
parser.add_argument('--ind', type=str, choices=["cr", "mpqa", "mr", "sst2", "subj", "trec"])
parser.add_argument('--ood', type=str, choices=["cr", "mpqa", "mr", "sst2", "subj", "trec"])
parser.add_argument('--dev_ind_size', type=int)
parser.add_argument('--val_ind_size', type=int)

args = argparse.Namespace(ind='trec', ood='sst2', dev_ind_size=500, val_ind_size=1000)

if __name__ == '__main__':
    raw_dataset_dir = Path('raw_dataset')
    dataset_dir = Path('dataset')

    if not dataset_dir.exists():
        dataset_dir.mkdir(parents=True)

    ind_dir = raw_dataset_dir / args.ind
    ood_dir = raw_dataset_dir / args.ood

    ind_config = Config(ind_dir / 'config.json')
    ind_all = []

    for key in ind_config.dict:
        ind_all.append(pd.read_csv(ind_config.dict.get(key), sep='\t'))
    else:
        ind_all = pd.concat(ind_all, ignore_index=True, sort=False)

    ood_config = Config(ood_dir / 'config.json')
    ood_all = []

    for key in ood_config.dict:
        ood_all.append(pd.read_csv(ood_config.dict.get(key), sep='\t'))
    else:
        ood_all = pd.concat(ood_all, ignore_index=True, sort=False)

    tr_ind, val_ind = train_test_split(ind_all, test_size=args.val_ind_size, random_state=777)
    tr_ind, dev_ind = train_test_split(tr_ind, test_size=args.dev_ind_size, random_state=777)

    tr_ood, val_ood = train_test_split(ood_all, test_size=args.val_ind_size, random_state=777)
    tr_ood, dev_ood = train_test_split(tr_ood, test_size=args.dev_ind_size, random_state=777)

    data_dir = dataset_dir / 'ind_{}_ood_{}'.format(args.ind, args.ood)

    if not data_dir.exists():
        data_dir.mkdir(parents=True)

    tr_ind_path = str(data_dir / 'tr_ind_{}.txt'.format(len(tr_ind)))
    dev_ind_path = str(data_dir / 'dev_ind_{}.txt'.format(len(dev_ind)))
    val_ind_path = str(data_dir / 'val_ind_{}.txt'.format(len(val_ind)))
    tr_ood_path = str(data_dir / 'tr_ood_{}.txt'.format(len(tr_ood)))
    dev_ood_path = str(data_dir / 'dev_ood_{}.txt'.format(len(dev_ood)))
    val_ood_path = str(data_dir / 'val_ood_{}.txt'.format(len(val_ood)))

    tr_ind.to_csv(tr_ind_path, sep='\t', index=False)
    dev_ind.to_csv(dev_ind_path, sep='\t', index=False)
    val_ind.to_csv(val_ind_path, sep='\t', index=False)

    tr_ood.to_csv(tr_ood_path, sep='\t', index=False)
    dev_ood.to_csv(dev_ood_path, sep='\t', index=False)
    val_ood.to_csv(val_ood_path, sep='\t', index=False)

    data_config = Config({'tr_ind': tr_ind_path,
                     'dev_ind': dev_ind_path,
                     'val_ind': val_ind_path,
                     'tr_ood': tr_ood_path,
                     'dev_ood': dev_ood_path,
                     'val_ood': val_ood_path})
    data_config.save(data_dir / 'config.json')

    experiment_dir = Path('experiments') / 'ind_{}_ood_{}'.format(args.ind, args.ood)

    if not experiment_dir.exists():
        experiment_dir.mkdir(parents=True)