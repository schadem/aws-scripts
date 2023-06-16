for number in {1..63}; do
    if ((number < 10)); then
        padded_number=$(printf "%02d" "$number")
    else
        padded_number=$number
    fi
    filename="s3://arxiv/pdf/arXiv_pdf_97${padded_number}_001.tar"
    aws s3 cp ${filename} ~/downloads/ --request-payer requester
done
